

from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token):
    try:
        user_token = Token.objects.get(key=token)
        return user_token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode('utf-8')
        all_queries = {}
        if query_string:
            query_string = query_string.split('&')
            for q_str in query_string:
                q_str = q_str.split('=')
                if len(q_str) > 0:
                    all_queries[q_str[0]] = q_str[1]

        if 'token' in all_queries:
            scope['user'] = await get_user(all_queries['token'])
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)