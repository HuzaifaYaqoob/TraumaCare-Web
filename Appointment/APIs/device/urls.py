

from django.urls import path, include

from . import views

urlpatterns = [
    path('get_my_appointments/', views.getMyAppointments ),
] 