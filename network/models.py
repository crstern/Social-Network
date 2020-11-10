from django.contrib.auth.models import AbstractUser
from django.db import models
import time



class User(AbstractUser):
    followers = models.ManyToManyField("User", related_name="following_users")
    following = models.ManyToManyField("User", related_name="follower_users")
    liked_posts = models.ManyToManyField("Post", related_name="liked", blank=True, null=True)
    def serialize(self):
        return {
            "username": self.username,
            "noFollowers": self.followers.count(),
            "noFollowing": self.following.count(),
        }



class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.CharField(max_length=1024)
    like_counter = models.IntegerField(default=0)
    comments = models.ManyToManyField("Comment", related_name="comment", blank=True)
    timestamp = models.DateTimeField( null=True, blank=True)

    def serialize(self):
        return {
            "author": self.author.username,
            "body": self.body,
            "comments": [comment.body for comment in self.comments.all()],
            "timestamp": str(self.timestamp).replace(" ", ""),
            "day": self.timestamp.day,
            "month": self.timestamp.month,
            "year": self.timestamp.year
        }

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)




