from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Chat(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    chat_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    thread_id = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('chat-detail',kwargs={'pk':self.pk})

