from django.urls import path
from django.conf.urls import include
from .views import GenerateRSSFeed, RunScript

urlpatterns = [
    path('run-script/', RunScript.as_view(), name='run_script'),
    path('rss-feed/', GenerateRSSFeed.as_view(), name='generate_rss_feed'),
]