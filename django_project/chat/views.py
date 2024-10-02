from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Chat

# Create your views here.


@login_required
def home(request):
    context = {"chats": Chat.objects.all()}
    return render(request, "chat/home.html", context)


class ChatListView(ListView):
    queryset = Chat.objects.all()
    template_name = "chat/home.html"  # Default - <app>/<model>_<viewtype>.html
    context_object_name = "chats"
    ordering = ["-chat_date"]


class ChatDetailView(DetailView):
    queryset = Chat.objects.all()

class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ChatUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chat
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        chat = self.get_object()
        if self.request.user == chat.author:
            return True
        return False

class ChatDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chat
    success_url = '/'

    def test_func(self):
        chat = self.get_object()
        if self.request.user == chat.author:
            return True
        return False



def about(request):
    return render(request, "chat/about.html", {"title": "About"})
