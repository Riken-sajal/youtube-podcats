import datetime, time
import threading
from django.core.management.base import BaseCommand
from driver.Upload_podcast import upload_podcast

class Command(BaseCommand):
    help = 'Upload podcast'

    def handle(self, *args, **kwargs):
        def run_podcast_upload():
            podcast_class = upload_podcast()
            
            last_login_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
            last_upload_time = datetime.datetime.now() - datetime.timedelta(hours=10)
            first_upload = True
            while True:
                current_time = datetime.datetime.now()
                if (current_time - last_login_time).total_seconds() >= 5 * 60:
                    podcast_class.login_apple()
                    last_login_time = current_time
                
                if ((current_time - last_upload_time).total_seconds() >= 10 * 60 * 60) or first_upload:
                    # podcast_class.upload()
                    podcast_class.publish()
                    last_upload_time = current_time
                    first_upload = False
                
                time.sleep(1)
        
        thread = threading.Thread(target=run_podcast_upload)
        thread.daemon = True 
        thread.start()

        self.stdout.write("Podcast upload command started in the background.")
