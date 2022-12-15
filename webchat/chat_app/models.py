from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    name = models.SlugField(max_length=30)
    users = models.ManyToManyField(User, related_name='users')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    invite = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(max_length=1024)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
