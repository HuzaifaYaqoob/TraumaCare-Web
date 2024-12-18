"""
ASGI config for TraumaCare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from TraumaCare.Middlewares.SocketMiddlewares import TokenAuthMiddleware

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TraumaCare.settings')
django.setup()

# import ChatXpo.Sockets.Routing.MainRouting
import Meet.websockets.urls

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    "websocket": TokenAuthMiddleware(URLRouter(Meet.websockets.urls.websocket_urls)
    ),
})

# ChatXpo.Sockets.Routing.MainRouting.websocket_urlpatterns,