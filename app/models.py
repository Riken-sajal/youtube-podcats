from django.db import models

# Create your models here.

class AudioFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='audio_files/')
    youtube_url = models.URLField()
    published_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
