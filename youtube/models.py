from django.db import models

# Create your models here.
class YouTobeModel(models.Model):
    video_id = models.CharField(max_length=100, unique=True, db_index=True)
    channelTitle = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    viewCount = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.video_id