import random
import time

from celery import shared_task
from .download_mp3 import download_youtube_audio, get_video_metadata
from app.models import AudioFile
import os

def process_video_urls(video_urls, output_dir):
    exists_videos_url = AudioFile.objects.values_list('youtube_url', flat=True)

    for video_url in video_urls:
        if video_url in exists_videos_url: continue

        try:
            metadata = get_video_metadata(video_url)

            download_info = download_youtube_audio(video_url,os.path.join(output_dir,'audio_files') )

            new_name = video_url.split('=')[-1]
            audio_file_path =  download_info['file_path']

            if not os.path.exists(audio_file_path) :
                print("The downloaded file doesn't exists")
                continue

            new_video_path = os.path.join(output_dir, 'audio_files', f"{new_name}.mp3")
            os.rename(audio_file_path, new_video_path)
            time.sleep(random.randint(5,10))
            length_in_seconds = download_info['length_in_seconds']
            cover_image_path = os.path.join('cover_imgs', "csvvc.jpg")
            new_video_path = os.path.join( 'audio_files', f"{new_name}.mp3")
            AudioFile.objects.create(
                title=metadata['title'],
                description=metadata['description'],
                category=metadata['category'],
                file=new_video_path,
                length_in_seconds=length_in_seconds,
                cover_image=cover_image_path,
                youtube_url=video_url,
                media_path=new_video_path
                
            )
        except Exception as e:
            # Log the error
            print(f"Error processing {video_url}: {str(e)}")