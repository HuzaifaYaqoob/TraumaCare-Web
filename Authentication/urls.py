
from django.urls import path


from .views import LoginPage, HospitalLoginPage, ResetPasswordPage, ChangePasswordHandler, RegisterPage, HandleJoin, ForgotPasswordPage, ForgotPasswordHandler, HandleLogin, HandleLogout, OtpVerificationPage, handleOtp, AutoLoginRedirection, CreateNewBusinessProfileRedirection

urlpatterns = [
    path('login/', LoginPage, name='LoginPage'),
    path('hospital_login/', HospitalLoginPage, name='HospitalLoginPage'),
    path('join/', RegisterPage, name='RegisterPage'),
    path('forgot-password/', ForgotPasswordPage, name='ForgotPasswordPage'),
    path('verification/otp/', OtpVerificationPage, name='OtpVerificationPage'),
    path('reset-password/', ResetPasswordPage, name='ResetPasswordPage'),


    path('auto-login-redirection/', AutoLoginRedirection, name='AutoLoginRedirection'),
    path('create-new-business-profile-redirection/', CreateNewBusinessProfileRedirection, name='CreateNewBusinessProfileRedirection'),

    path('logout-handler/', HandleLogout, name='HandleLogout'),
    path('login-handler/', HandleLogin, name='HandleLogin'),
    path('join-handler/', HandleJoin, name='HandleJoin'),
    path('forgot-password-handler/', ForgotPasswordHandler, name='ForgotPasswordHandler'),
    path('change-password-handler/', ChangePasswordHandler, name='ChangePasswordHandler'),
    path('otp-handler/', handleOtp, name='handleOtp'),
] 
