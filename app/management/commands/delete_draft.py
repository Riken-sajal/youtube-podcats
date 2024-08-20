from driver.Upload_podcast import upload_podcast
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        podcast_class = upload_podcast()
        
        podcast_class.login_apple()
        podcast_class.delete_drafts()
        