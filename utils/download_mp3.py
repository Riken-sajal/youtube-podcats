import os
import yt_dlp as youtube_dl
from mutagen.mp3 import MP3

def get_video_metadata(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        metadata = {
            'title': info['title'],
            'description': info.get('description', ''),
            'category': info.get('categories', ['Unknown'])[0],
        }
    return metadata

def download_youtube_audio(video_url, output_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ffmpeg_location': '/usr/bin/ffmpeg'  # Adjust this path if necessary
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = os.path.join(output_dir, f"{info['title']}.mp3")
        audio = MP3(file_path)
        length_in_seconds = int(audio.info.length)
        
        
        return {
            'file_path': file_path,
            'length_in_seconds': length_in_seconds
        }
