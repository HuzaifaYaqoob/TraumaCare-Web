
from django.urls import path

from . import views

urlpatterns = [
    # path('create_video_chat/', views.create_video_chat),
    path('get_video_chat/', views.get_video_chat),
    # path('get_user_video_chats/', views.get_user_video_chats),
]
