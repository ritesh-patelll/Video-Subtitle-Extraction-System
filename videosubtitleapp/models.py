import os
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='videos/')
    subtitles = models.FileField(upload_to='subtitles/', blank=True, null=True)

    def get_subtitles_path(self):
        return '{}.srt'.format(os.path.splitext(self.file.name)[0])