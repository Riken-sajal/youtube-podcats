# podcast/views.py
from django.views import View
from .models import AudioFile
from utils.download_mp3 import download_youtube_audio
from utils.rss_feed import create_rss_feed
from django.http import JsonResponse, HttpResponse
import os
from driver.bot import Driver_bot


class RunScript(View):
    def get(self, request, *args, **kwargs):
        output_dir = os.path.join(os.getcwd(), 'media/audio_files')
        os.makedirs(output_dir, exist_ok=True)

        driver_cls = Driver_bot()
        channel_name = "RanveerAllahbadia"
        all_videos_link = driver_cls.main(channel_name)

        for video_url in all_videos_link:
            try:
                audio_file_name = download_youtube_audio(video_url, output_dir)
                audio_file_path = os.path.join('audio_files', audio_file_name)
                AudioFile.objects.create(
                    title=audio_file_name,
                    file=audio_file_path,
                    youtube_url=video_url
                )
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Audio files downloaded and saved successfully'}, status=200)


class GenerateRSSFeed(View):
    def get(self, request, *args, **kwargs):
        audio_files = AudioFile.objects.all()
        base_url = request.build_absolute_uri('/')
        rss_feed_content = create_rss_feed(audio_files, base_url)
        return HttpResponse(rss_feed_content, content_type='application/rss+xml')
