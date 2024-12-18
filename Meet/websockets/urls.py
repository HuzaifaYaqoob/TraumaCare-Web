
from django.urls import path

from .consumers.VideoChatConsumers import VideoChatConsumers, ActivatedVideoChat
from .consumers.userConsumers import UserConsumer

websocket_urls = [
    path('ws/user/<str:user_id>/' , UserConsumer.as_asgi() ),
    path('ws/video-chat/<str:videochat_id>/' , VideoChatConsumers.as_asgi() ),
    path('ws/video-chat/<str:videochat_id>/activated/' , ActivatedVideoChat.as_asgi() ),
]