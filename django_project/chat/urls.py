from django.urls import path
from . import views
from .views import ChatListView, ChatDetailView, ChatCreateView, ChatDeleteView, ChatUpdateView

urlpatterns = [
    path('', ChatListView.as_view(), name='chat-home'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chat/new/', ChatCreateView.as_view(), name='chat-create'),
    path('chat/<int:pk>/update/', ChatUpdateView.as_view(), name='chat-update'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat-delete'),
    path('about/', views.about, name='chat-about'),
]