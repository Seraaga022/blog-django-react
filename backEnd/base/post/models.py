from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

class Tag(models.Model):
    name = models.TextField(unique=True)

class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    img = models.TextField(default='empty')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    backGround_color = models.TextField(default='39465e')
    text_color = models.TextField(default='ffffff')

