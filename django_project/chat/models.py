from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    chat_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

