# app/views.py
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from utils.rss_feed import create_rss_feed
from app.models import AudioFile
import os
import json
from driver.bot import Driver_bot
from driver.Upload_podcast import upload_podcast
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.tasks import process_video_urls


@method_decorator(csrf_exempt, name='dispatch')
class RunScript(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            channel_name = data.get('channel_name')
            if not channel_name:
                return JsonResponse({'error': 'Channel name is required'}, status=400)

            driver_cls = Driver_bot()
            video_urls = driver_cls.main(channel_name)
            driver_cls.Close_driver()
            if not video_urls:
                return JsonResponse({'error': 'No videos found for this channel'}, status=404)

            output_dir = os.path.join(os.getcwd(), 'media')
            os.makedirs(output_dir, exist_ok=True)

            # Schedule the background task
            process_video_urls(video_urls, output_dir)

            return JsonResponse({'message': 'Audio files download started in background'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class GenerateRSSFeed(View):
    def get(self, request, *args, **kwargs):
        audio_files = AudioFile.objects.all()
        base_url = request.build_absolute_uri('/')[:-1]
        rss_feed_content = create_rss_feed(audio_files, base_url)
        return HttpResponse(rss_feed_content, content_type='application/rss+xml')
