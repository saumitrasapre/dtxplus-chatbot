from django.urls import path
from . import views
from .views import ChatListView, ChatDeleteView, ChatUpdateView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-home'),
    path('start-new-chat/', views.start_new_chat, name='start_new_chat'),
    path('save-chat/', views.save_chat, name='save_chat'),
    path('get-chat/<int:chat_id>/', views.get_chat, name='get_chat'),
    path('clear-chat/', views.clear_chat, name='clear_chat'),
    path('chat-history-partial/', views.chat_history_partial, name='chat_history_partial'),
    path('chat/<int:pk>/update/', ChatUpdateView.as_view(), name='chat-update'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat-delete'),
    path('about/', views.about, name='chat-about'),
]