from django.db import models

# Create your models here.
class YouTobeModel(models.Model):
    video_id = models.CharField(max_length=100, unique=True, db_index=True)
    channelTitle = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    viewCount = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.video_id
    

class Comment(models.Model):
    text_id = models.TextField()
    text = models.TextField()
    date = models.DateTimeField()
    author = models.CharField(max_length = 1000)
    author_info = models.CharField(max_length=1000)
    author_profile_url = models.URLField()

    def __str__(self):
        return self.text
