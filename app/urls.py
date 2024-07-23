from django.urls import path
from .views import RunScript, GenerateRSSFeed

urlpatterns = [
    path('run-script/', RunScript.as_view(), name='run_script'),
    path('rss-feed/', GenerateRSSFeed.as_view(), name='generate_rss_feed'),
]