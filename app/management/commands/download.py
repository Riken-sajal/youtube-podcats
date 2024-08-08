from django.core.management.base import BaseCommand
import os, random, time
from app.models import AudioFile, Videos
from podcast.settings import output_dir
from driver.login_mail import Google
from mutagen.mp3 import MP3

class Command(BaseCommand):
    help = 'Upload podcast'

    def handle(self, *args, **kwargs):
        self.exists_videos_url = AudioFile.objects.values_list('youtube_url', flat=True) 
        
        metadata = self.download_video(self.get_video_link())
        if metadata :
            self.video_object.download_done = True
            self.video_object.save()
            self.save_video_data(metadata)
        
    def get_video_link(self):
        self.video_object = Videos.objects.filter(download_done=False).order_by('created_at').first()
        return  self.video_object
    
    def download_video(self,video_object):
        if not video_object :
            raise "The video object to be downloaded is NONE"
        
        video_downloaded = self.check_video_downloaded()
        data = self.get_videos_data()
        self.video_object.download_done = True
        self.video_object.save()
        self.save_video_data(data)
        
    def get_videos_data(self):
        Google_class = Google()
        data = Google_class.videos_data(self.video_object.url)
        Google_class.download_videos(self.video_object.url)
        
        download_dir = '/home/ubuntu/Downloads'

        for file in os.listdir(download_dir) :
            if data['title'] in file :
                file_path = os.path.join(download_dir, file)
                while True :
                    if not ".crdownload" in file_path :
                        break
                    elif not os.path.exists(file_path):
                        print(os.path.exists(file_path))
                        break
                    else:
                        print("file could not found")
                        print(os.listdir(download_dir) )
                        time.sleep(1)
                print(file_path)
                break
        else :
            return
        
        new_name = self.video_object.url.split('=')[-1]
        new_video_path = os.path.join(output_dir, f"{new_name}.mp3")
        
                
        os.rename(file_path, new_video_path)
        data['file_path'] = new_video_path
        audio = MP3(new_video_path)
        data['length_in_seconds'] = audio.info.length
        return data
        
    def move_videos(self):
        os.listdir("~/Downloads/")
        pass

    def save_video_data(self,metadata):
        """Save downloaded videos details into the object"""
        
        
        new_name = self.video_object.url.split('=')[-1]
        if not self.check_video_downloaded():
            new_video_path = os.path.join(output_dir, f"{new_name}.mp3")
            breakpoint()
            os.rename(metadata['file_path'], new_video_path)
            time.sleep(random.randint(5,10))
        
        length_in_seconds = metadata['length_in_seconds']
        cover_image_path = os.path.join('cover_imgs', "csvvc.jpg")
        new_video_path = os.path.join( 'audio_files', f"{new_name}.mp3")
        Audio_obj = AudioFile.objects.create(
            title=metadata['title'],
            description=metadata['description'],
            category=metadata['category'],
            file=new_video_path,
            length_in_seconds=length_in_seconds,
            cover_image=cover_image_path,
            youtube_url=self.video_object.url,
            media_path=new_video_path,
            video = self.video_object
        )
        
        return Audio_obj
    
    def check_video_downloaded(self):
        """
        Checking the video is already downloaded or not
        return :
        if video downloaded return True
        else return False
        
        to allow the download process
        """
        if  os.path.exists(os.path.join(output_dir, f"{self.video_object.url.split('=')[-1]}.mp3")):
            return True
        else :
            return False