# app/views.py
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from utils.rss_feed import create_rss_feed
from app.models import AudioFile, TwoFactorCode, Videos
from django.utils import timezone
import os, json
from driver.bot import Driver_bot
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.tasks import process_video_urls
from podcast.settings import output_dir
from driver.login_mail import Google

@method_decorator(csrf_exempt, name='dispatch')
class RunScript(View):
    def post(self, request, *args, **kwargs):
        
        def create_video_obj(vd_url:str = ""):
            if not vd_url : return False

            vd_obj = Videos.objects.get_or_create(
                url = vd_url,
                download_done = False
            )
            return vd_obj
        
        try:
            data = json.loads(request.body)
            channel_name = data.get('channel_name')
            if not channel_name:
                return JsonResponse({'error': 'Channel name is required'}, status=400)

            Google_cls = Google()
            video_urls = Google_cls.collect_videos(channel_name)
            Google_cls.Close_driver()
            
            if not video_urls:
                return JsonResponse({'error': 'No videos found for this channel'}, status=404)

            for video_url in video_urls :
                create_video_obj(video_url)

            # Schedule the background task
            # process_video_urls(video_urls, output_dir)

            return JsonResponse({'message': 'Audio files will be starting download in background'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error : {e}'}, status=400)

class GenerateRSSFeed(View):
    def get(self, request,identifier, *args, **kwargs):
        audio_files = AudioFile.objects.filter(uploaded_podcast = False)
        if not audio_files :
            return JsonResponse({'error': f'Error : All podcast has been uploaded'}, status=400)
        
        base_url = request.build_absolute_uri('/')[:-1]
        rss_feed_content = create_rss_feed(audio_files, base_url)
        return HttpResponse(rss_feed_content, content_type='application/rss+xml')

two_factor_code = None

@csrf_exempt
def submit_2fa_code(request):
    global two_factor_code
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        if code:
            TwoFactorCode.objects.all().delete()  # Clear previous codes
            TwoFactorCode.objects.create(code=code, created_at=timezone.now())
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

