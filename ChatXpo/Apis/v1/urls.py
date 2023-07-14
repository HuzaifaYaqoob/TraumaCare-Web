
from django.urls import path



from .views import create_new_chat, get_user_chat_list, get_chat_messages

urlpatterns = [
    path('create_new_chat/', create_new_chat),
    path('get_user_chat_list/', get_user_chat_list),

    path('get_chat_messages/', get_chat_messages),
] 