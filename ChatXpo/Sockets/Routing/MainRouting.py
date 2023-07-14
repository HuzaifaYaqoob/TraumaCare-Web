

from django.urls import path

from ChatXpo.Sockets.Consumers.XpoComsumer import XpoConsumer

websocket_urlpatterns = [
    path('ws/user-chat-xpo/<str:user_id>', XpoConsumer.as_asgi())
]