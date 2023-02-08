
from django.urls import path


from . import views as doctor_views


urlpatterns = [
    path('search/', doctor_views.DoctorSearchPage, name='DoctorSearchPage'),
    path('profile/view/', doctor_views.DoctorProfilePage, name='DoctorProfilePage'),
] 