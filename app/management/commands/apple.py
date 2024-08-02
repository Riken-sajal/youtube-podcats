from django.core.management.base import BaseCommand
from driver.Upload_podcast import upload_podcast
class Command(BaseCommand):

    def handle(self, *args, **options):
        podcast_class = upload_podcast()
        podcast_class.login_apple()
        podcast_class.upload()