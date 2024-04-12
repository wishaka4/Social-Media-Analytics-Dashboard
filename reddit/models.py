from django.db import models

class RedditPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    score = models.IntegerField()
    num_comments = models.IntegerField()
    upvote_ratio = models.FloatField()
    selftext = models.TextField()
    link_flair_text = models.CharField(max_length=255)

    def __str__(self):
        return self.title
