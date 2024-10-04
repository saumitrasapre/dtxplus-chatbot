from typing import Any
import json
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .chatbot.memory.mem_operations import get_next_available_thread_id,clear_memory
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
from django.utils import timezone

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
    if 'new_chat_thread_id' in request.session:
        print("here")
        new_chat_thread_id = request.session['new_chat_thread_id']
        # If a thread id already exists in session, flush its memory
        clear_memory(thread_id=str(new_chat_thread_id))
    else:
        # Call the backend function to generate the chat ID
        new_chat_thread_id = str(get_next_available_thread_id())

        # Store the chat ID in the session
        request.session['new_chat_thread_id'] = new_chat_thread_id
        request.session.modified = True  # Mark the session as modified
        request.session.save()           # Save the session explicitly

    # Return the chat ID as JSON response
    return JsonResponse({'new_chat_thread_id': new_chat_thread_id})

@require_POST
def save_chat(request):
    data = json.loads(request.body)
    chat_messages = data.get('chat_messages', '')

    if chat_messages:
        # chat_summary, chat_title = summarize_chat(chat_messages)
        chat_title = f"Chat - {timezone.now().strftime('%d/%m/%Y - %H:%M:%S')}"

        if 'new_chat_thread_id' in request.session:
            thread_id = request.session['new_chat_thread_id']
        else:
            thread_id = get_next_available_thread_id()
        # Save the summary and title to the database
        new_chat = Chat.objects.create(
            author=request.user,
            title=chat_title,
            content="Chat content",
            thread_id = thread_id
        )

         # Call the backend function to generate the chat ID
        new_chat_thread_id = str(get_next_available_thread_id())

        # Store the chat ID in the session
        request.session['new_chat_thread_id'] = new_chat_thread_id
        request.session.modified = True  # Mark the session as modified
        request.session.save()           # Save the session explicitly

        return JsonResponse({
            'success': True,
            'chat_id': new_chat.id,
            'chat_title': chat_title
        })

    return JsonResponse({'success': False, 'error': 'No chat messages found'})

def chat_history_partial(request):
    chats = Chat.objects.filter(author=request.user)  # Assuming user-specific chat history
    return render(request, 'chat/partials/chat_history.html', {'chats': chats})

        
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
    
    def post(self, request, *args, **kwargs):
        """ Custom post logic to handle the deletion and run custom functions before the delete. """

        # Fetch the chat object to be deleted
        chat = self.get_object()

        # Custom actions before deletion:
        # 1. Clear memory related to the chat thread
        clear_memory(thread_id=str(chat.thread_id))
        
        # 2. Generate a new chat thread ID and store it in the session
        new_chat_thread_id = str(get_next_available_thread_id())
        request.session['new_chat_thread_id'] = new_chat_thread_id
        request.session.modified = True  # Mark session as modified to ensure it's saved
        request.session.save()           # Save the session explicitly

        # Log for debugging purposes
        print(f"New chat thread ID {new_chat_thread_id} set in session.")

        # Proceed with the actual deletion of the object
        response = super().post(request, *args, **kwargs)

        # Log confirmation of deletion
        print(f"Chat {chat.thread_id} deleted successfully.")

        # Return the standard DeleteView response (redirect to success_url)
        return response



def about(request):
    return render(request, "chat/about.html", {"title": "About"})
