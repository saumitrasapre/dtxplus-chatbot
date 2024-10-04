from django.urls import path
from . import views
from .views import ChatListView, ChatDetailView, ChatCreateView, ChatDeleteView, ChatUpdateView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-home'),
    path('start-new-chat/', views.start_new_chat, name='start_new_chat'),
    path('save-chat/', views.save_chat, name='save_chat'),
    path('chat-history-partial/', views.chat_history_partial, name='chat_history_partial'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chat/new/', ChatCreateView.as_view(), name='chat-create'),
    path('chat/<int:pk>/update/', ChatUpdateView.as_view(), name='chat-update'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat-delete'),
    path('about/', views.about, name='chat-about'),
]