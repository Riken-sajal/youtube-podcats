# management/commands/upload_podcast_command.py

from django.core.management.base import BaseCommand
from driver.Upload_podcast import upload_podcast

class Command(BaseCommand):
    help = 'Upload podcast'

    def handle(self, *args, **kwargs):
        podcast_class = upload_podcast()
        podcast_class.login_apple()
        podcast_class.upload()
