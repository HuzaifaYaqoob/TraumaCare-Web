
from django.urls import path


from .views import LoginPage, RegisterPage, HandleJoin

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
] 