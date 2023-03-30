
from django.urls import path


from .views import LoginPage, RegisterPage, HandleJoin, HandleLogin, HandleLogout

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
    path('verification/otp/', RegisterPage, name='RegisterPage'),

    path('logout-handler/', HandleLogout, name='HandleLogout'),
    path('login-handler/', HandleLogin, name='HandleLogin'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
] 
