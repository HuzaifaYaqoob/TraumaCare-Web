
from django.urls import path


from .views import LoginPage, RegisterPage

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
] 