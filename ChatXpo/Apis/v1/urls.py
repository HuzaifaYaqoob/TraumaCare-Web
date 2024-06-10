
from django.urls import path



from .views import create_new_chat, get_user_chat_list, get_chat_messages, send_chat_widget_message

urlpatterns = [
    path('create_new_chat/', create_new_chat),
    path('get_user_chat_list/', get_user_chat_list),

    path('get_chat_messages/', get_chat_messages),
    path('send_chat_widget_message/<str:chatId>/', send_chat_widget_message),
] 