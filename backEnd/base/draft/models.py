from django.db import models

class Draft(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    img = models.TextField(default='empty')

class DraftCategory(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    category = models.ForeignKey('post.Category', on_delete=models.CASCADE)

class DraftTag(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    tag = models.ForeignKey('post.Tag', on_delete=models.CASCADE)
    backGround_color = models.TextField(default='39465e')
    text_color = models.TextField(default='ffffff')
