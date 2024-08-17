# management/commands/upload_podcast_command.py
import datetime, time
from django.core.management.base import BaseCommand
from driver.Upload_podcast import upload_podcast

class Command(BaseCommand):
    help = 'Upload podcast'

    def handle(self, *args, **kwargs):
        podcast_class = upload_podcast()
        
        # Initialize the start time for both tasks
        last_login_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
        last_upload_time = datetime.datetime.now() - datetime.timedelta(hours=10)
        first_upload = True
        while True:
            
            current_time = datetime.datetime.now()
            breakpoint()
            if (current_time - last_login_time).total_seconds() >= 5 * 60:
                podcast_class.login_apple()
                last_login_time = current_time
            
            if ((current_time - last_upload_time).total_seconds() >= 10 * 60 * 60) or first_upload:
                podcast_class.upload()
                podcast_class.publish()
                last_upload_time = current_time
                first_upload = False
            
            # Sleep for a short period to prevent high CPU usage
            time.sleep(1)