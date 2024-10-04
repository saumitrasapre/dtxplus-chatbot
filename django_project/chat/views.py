from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .chatbot.memory.mem_operations import get_next_available_thread_id
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Chat

# Create your views here.

class ChatListView(LoginRequiredMixin,ListView):
    model = Chat
    template_name = "chat/home.html"  # Default - <app>/<model>_<viewtype>.html
    context_object_name = "chats"

    # Handle chats
    def handle_chat(self):
        # Perform your custom logic here
        return "This function handles chat"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return Chat.objects.filter(author=user).order_by("-chat_date")
    
    def get_context_data(self, **kwargs):
        # Get the default context data from ListView
        context = super().get_context_data(**kwargs)
        
        # Add custom data using your custom function
        context['chat_msg'] = self.handle_chat()
        
        return context

@require_POST
def start_new_chat(request):
    # Call your backend function to generate the chat ID
    new_chat_id = str(get_next_available_thread_id())

    # Store the chat ID in the session
    request.session['new_chat_id'] = new_chat_id

    # Return the chat ID as JSON response
    return JsonResponse({'new_chat_id': new_chat_id})

        
class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return Chat.objects.filter(author=user).order_by("-chat_date")

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
