
from django.urls import path



from .views import create_new_chat

urlpatterns = [
    path('create_new_chat/', create_new_chat,)
] 