from django.shortcuts import render
from .models import Chat

# Create your views here.

def home(request):
    context = {
        'chats': Chat.objects.all()
    }
    return render(request,'chat/home.html', context)

def about(request):
    return render(request,'chat/about.html',{'title':'About'})