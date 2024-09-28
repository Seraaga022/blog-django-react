from django.db import models
from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)