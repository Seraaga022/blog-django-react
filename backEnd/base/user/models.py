from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.TextField(unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    img = models.TextField(default='blank-img.png')
    role = models.TextField(default='customer') # customer, user
    def cor():
        return 'hello'