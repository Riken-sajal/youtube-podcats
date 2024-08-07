from django.core.management.base import BaseCommand
from driver.Upload_podcast import upload_podcast
from app.models import AudioFile
from app.views import GenerateRSSFeed
from django.test import RequestFactory

class Command(BaseCommand):

    def handle(self, *args, **options):
        factory = RequestFactory()
        request = factory.get("/podcast/rss-feed/")
        response = GenerateRSSFeed.as_view()(request)
        if response.status_code == 200:
            rss_feed_content = response.content
            self.stdout.write(self.style.SUCCESS('Successfully generated RSS feed'))
            # Optionally, save the RSS feed content to a file
            with open('rss_feed.xml', 'wb') as f:
                f.write(rss_feed_content)

        else:
            self.stdout.write(self.style.ERROR('Failed to generate RSS feed'))
