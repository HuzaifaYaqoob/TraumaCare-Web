
from django.urls import path


from .views import LoginPage, RegisterPage, HandleJoin, HandleLogin, HandleLogout, OtpVerificationPage, handleOtp, AutoLoginRedirection

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
    path('verification/otp/', OtpVerificationPage, name='OtpVerificationPage'),


    path('auto-login-redirection/', AutoLoginRedirection, name='AutoLoginRedirection'),

    path('logout-handler/', HandleLogout, name='HandleLogout'),
    path('login-handler/', HandleLogin, name='HandleLogin'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
    path('otp-handler/', handleOtp, name='handleOtp'),
] 
