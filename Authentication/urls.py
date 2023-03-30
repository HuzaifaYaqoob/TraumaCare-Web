
from django.urls import path


from .views import LoginPage, RegisterPage, HandleJoin, HandleLogin, HandleLogout, OtpVerificationPage

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
    path('verification/otp/', OtpVerificationPage, name='OtpVerificationPage'),

    path('logout-handler/', HandleLogout, name='HandleLogout'),
    path('login-handler/', HandleLogin, name='HandleLogin'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
] 
