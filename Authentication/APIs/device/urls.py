

from django.urls import path, include

from . import views

urlpatterns = [
    path('handle_login/', views.HandleLogin ),
    path('handle_otp_verification/', views.HandleOtpVerification ),

] 