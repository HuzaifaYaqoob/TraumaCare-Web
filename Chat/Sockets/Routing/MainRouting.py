

from django.urls import path

from Chat.Sockets.Consumers.UserConsumer import UserConsumer_Socket

websocket_urlpatterns = [
    path('ws/user-chat/<str:user_id>', UserConsumer_Socket.as_asgi())
]