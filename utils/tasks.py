from celery import shared_task
from .download_mp3 import download_youtube_audio, get_video_metadata
from app.models import AudioFile
import os

@shared_task
def process_video_urls(video_urls, output_dir):
    for video_url in video_urls:
        try:
            metadata = get_video_metadata(video_url)
            audio_file_name = download_youtube_audio(video_url, output_dir)
            audio_file_path = os.path.join('audio_files', audio_file_name)
            AudioFile.objects.create(
                title=metadata['title'],
                description=metadata['description'],
                category=metadata['category'],
                file=audio_file_path,
                youtube_url=video_url
            )
        except Exception as e:
            # Log the error
            print(f"Error processing {video_url}: {str(e)}")