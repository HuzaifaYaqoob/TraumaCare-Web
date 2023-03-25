
from django.urls import path


from .views import LoginPage, RegisterPage, HandleJoin, HandleLogin

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),

    path('login-handler/', HandleLogin, name='HandleLogin'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
] 