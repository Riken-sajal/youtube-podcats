from django.db import models
import os

# Create your models here.


class Videos(models.Model):
    url = models.URLField()
    download_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.url.split("=")[-1]

class AudioFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='audio_files/')
    media_path = models.CharField(blank=True, null=True, default='', max_length=255)
    cover_image = models.FileField(upload_to='cover_imgs/', default=os.path.join('cover_imgs', "csvvc.jpg"))
    youtube_url = models.URLField()
    length_in_seconds = models.IntegerField()
    published_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_podcast = models.BooleanField(default=False)
    video = models.ForeignKey('Videos', on_delete=models.CASCADE)
    rss_url = models.CharField(blank=True, null=True, default='', max_length=522)

    def __str__(self):
        self.media_path = os.path.join('media', 'audio_files', self.title)
        self.rss_url = self.youtube_id()
        return self.title

    def youtube_id(self):
        # Extracts the video ID from the youtube_url
        if 'youtu.be' in self.youtube_url:
            return self.youtube_url.split('/')[-1]
        elif 'youtube.com' in self.youtube_url:
            return self.youtube_url.split('v=')[-1].split('&')[0]
        return None
    
    
class TwoFactorCode(models.Model):
    code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)