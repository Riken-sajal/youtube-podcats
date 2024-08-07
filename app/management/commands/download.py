from django.core.management.base import BaseCommand
import os, random, time
from app.models import AudioFile, Videos
import yt_dlp as youtube_dl
from mutagen.mp3 import MP3
from podcast.settings import output_dir

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
        
        video_url = video_object.url
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'quiet': True,
            'no_warnings': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download= False if video_downloaded else True)
            if not video_downloaded :
                file_path = os.path.join(output_dir, f"{info['title']}.mp3")
                audio = MP3(file_path)
            else :
                file_path = os.path.join(output_dir, f"{self.video_object.url.split('=')[-1]}.mp3")
            
            return {
                'file_path': file_path,
                'length_in_seconds': info['duration'],
                'title': info['title'],
                'description': info.get('description', ''),
                'category': info.get('categories', ['Unknown'])[0]
            }

    def save_video_data(self,metadata):
        """Save downloaded videos details into the object"""
        
        
        if not self.check_video_downloaded():
            new_name = self.video_object.url.split('=')[-1]
            new_video_path = os.path.join(output_dir, f"{new_name}.mp3")
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