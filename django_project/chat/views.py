from typing import Any
import json
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .chatbot.memory.mem_operations import get_next_available_thread_id,clear_memory, get_latest_checkpoint_from_memory,parse_checkpoint_messages_for_UI 
from .chatbot.tools.summary_tool import summary_tool_parameterized
from django.views.generic import ListView
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

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return Chat.objects.filter(author=user).order_by("-chat_date")
    

@require_POST
def start_new_chat(request):
    if 'new_chat_thread_id' in request.session:
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
        chat_title = f"Chat - {timezone.now().strftime('%d/%m/%Y - %H:%M:%S')}"

        if 'new_chat_thread_id' in request.session:
            thread_id = request.session['new_chat_thread_id']
        else:
            thread_id = get_next_available_thread_id()
        
        if not Chat.objects.filter(thread_id=thread_id).exists():
            # Save the summary and title to the database
            new_chat = Chat.objects.create(
                author=request.user,
                title=chat_title,
                content="Chat content",
                thread_id = thread_id
            )
        else:
            new_chat = Chat.objects.filter(thread_id=thread_id).first()
            new_chat.title = chat_title
            new_chat.save()
        
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
    chats = Chat.objects.filter(author=request.user)
    return render(request, 'chat/partials/chat_history.html', {'chats': chats})


def get_chat(request, chat_id):
    # Fetch the chat messages based on chat_id
    thread_id = Chat.objects.filter(id=chat_id).first().thread_id
    chkpt = get_latest_checkpoint_from_memory(str(thread_id))
    if chkpt:
        formatted_messages = parse_checkpoint_messages_for_UI(chkpt['messages'])
        chat_summary = summary_tool_parameterized(formatted_messages)
        # Store the chat ID in the session
        request.session['new_chat_thread_id'] = thread_id
        request.session.modified = True  # Mark the session as modified
        request.session.save()           # Save the session explicitly
        formatted_messages['summary'] = chat_summary
        return JsonResponse(formatted_messages)
    else:
        messages_list = []
        print("Error retrieving messages")
        return JsonResponse({'messages': messages_list})
    

def refresh_summary(request):
    # Fetch the chat messages based on chat_id
    if 'new_chat_thread_id' in request.session:
        thread_id = request.session['new_chat_thread_id']
    else:
        thread_id = str(get_next_available_thread_id())
    chkpt = get_latest_checkpoint_from_memory(str(thread_id))
    if chkpt:
        formatted_messages = parse_checkpoint_messages_for_UI(chkpt['messages'])
        chat_summary = summary_tool_parameterized(formatted_messages)        
        return JsonResponse({'summary': chat_summary})
    else:
        summary = ''
        print("Error retrieving messages")
        return JsonResponse({'summary': summary})


def clear_chat(request):
    if 'new_chat_thread_id' in request.session:
        new_chat_thread_id = request.session['new_chat_thread_id']
    else:
        new_chat_thread_id = str(get_next_available_thread_id())
    
    clear_memory(thread_id=str(new_chat_thread_id))
    # Check if we have cleared a chat from history.
    if Chat.objects.filter(thread_id=new_chat_thread_id).exists():
        # If so, delete it from history.
            Chat.objects.filter(thread_id=new_chat_thread_id).delete()

    request.session['new_chat_thread_id'] = new_chat_thread_id
    request.session.modified = True  # Mark the session as modified
    request.session.save()           # Save the session explicitly
    return JsonResponse({
            'success': True,
            'chat_id': new_chat_thread_id,
    })
   


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

        print(f"New chat thread ID {new_chat_thread_id} set in session.")

        # Proceed with the actual deletion of the object
        response = super().post(request, *args, **kwargs)

        print(f"Chat {chat.thread_id} deleted successfully.")

        # Return the standard DeleteView response (redirect to success_url)
        return response



def about(request):
    return render(request, "chat/about.html", {"title": "About"})
