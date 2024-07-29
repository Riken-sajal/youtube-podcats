from celery import shared_task
from .download_mp3 import download_youtube_audio, get_video_metadata
from app.models import AudioFile
import os

def process_video_urls(video_urls, output_dir):
    for video_url in video_urls:
        try:
            print('----1')
            metadata = get_video_metadata(video_url)
            print('----2')
            
            download_info = download_youtube_audio(video_url,os.path.join(output_dir,'audio_files') )
            
            audio_file_path =  download_info['file_path']
            length_in_seconds = download_info['length_in_seconds']
            cover_image_path = os.path.join(output_dir,'cover_imgs', "csvvc.jpg")
            AudioFile.objects.create(
                title=metadata['title'],
                description=metadata['description'],
                category=metadata['category'],
                file=audio_file_path,
                length_in_seconds = length_in_seconds,
                cover_image=cover_image_path,
                youtube_url=video_url,
                media_path = os.path.join('media','audio_files',metadata['title'])
                
            )
        except Exception as e:
            # Log the error
            print(f"Error processing {video_url}: {str(e)}")