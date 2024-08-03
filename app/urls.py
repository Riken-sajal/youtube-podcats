from django.urls import path
from .views import RunScript, GenerateRSSFeed, submit_2fa_code

urlpatterns = [
    path('run-script/', RunScript.as_view(), name='run_script'),
    path('rss-feed/', GenerateRSSFeed.as_view(), name='generate_rss_feed'),
    path('submit-2fa-code/', submit_2fa_code, name='submit-2fa-code'),
]