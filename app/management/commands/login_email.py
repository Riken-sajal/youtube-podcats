# management/commands/upload_podcast_command.py

from django.core.management.base import BaseCommand
from driver.login_mail import Google

class Command(BaseCommand):
    help = 'Upload podcast'

    def handle(self, *args, **kwargs):
        Google_class = Google()
        print(Google_class.collect_videos(channel_name="rikenkhadela9654"))
