from django.db import models

# Create your models here.

class AudioFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='audio_files/')
    youtube_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
