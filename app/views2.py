# podcast/views.py
from django.views import View
from .models import AudioFile
from utils.download_mp3 import download_youtube_audio, get_video_metadata
from utils.rss_feed import create_rss_feed
from django.http import JsonResponse, HttpResponse
import os, json
from driver.bot import Driver_bot
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.tasks import process_video_urls


class RunScript(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
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

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            channel_name = data.get('channel_name')
            if not channel_name:
                return JsonResponse({'error': 'Channel name is required'}, status=400)

            driver_cls = Driver_bot()
            video_urls = driver_cls.main(channel_name)
            if not video_urls:
                return JsonResponse({'error': 'No videos found for this channel'}, status=404)

            output_dir = os.path.join(os.getcwd(), 'media/audio_files')
            os.makedirs(output_dir, exist_ok=True)

            # Schedule the background task
            process_video_urls.delay(video_urls, output_dir)

            return JsonResponse({'message': 'Audio files download started in background'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class GenerateRSSFeed(View):
    def get(self, request, *args, **kwargs):
        audio_files = AudioFile.objects.all()
        base_url = request.build_absolute_uri('/')[:-1]
        rss_feed_content = create_rss_feed(audio_files, base_url)
        return HttpResponse(rss_feed_content, content_type='application/rss+xml')
