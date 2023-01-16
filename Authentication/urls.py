
from django.urls import path


from .views import LoginPage

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
] 