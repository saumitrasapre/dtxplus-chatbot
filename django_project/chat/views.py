from django.shortcuts import render

# Create your views here.

posts = [
    {
        'author':'user1',
        'title':'Post 1',
        'content':'First post content',
        'date_posted':'August 27, 2024',
    },
    {
        'author':'user2',
        'title':'Post 2',
        'content':'Second post content',
        'date_posted':'August 28, 2024',
    },
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request,'chat/home.html', context)

def about(request):
    return render(request,'chat/about.html',{'title':'About'})