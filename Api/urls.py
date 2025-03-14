
from django.urls import path, include

from . import views

urlpatterns = [

    path('', include('Trauma.APIs.v1.urls') ),
    path('v1/get_location_distance/', views.get_location_distance, name='get_location_distance'),

    path('v1/auth/', include('Authentication.APIs.v1.urls') ),
    path('device/auth/', include('Authentication.APIs.device.urls') ),

    path('v1/chatxpo/', include('ChatXpo.Apis.v1.urls') ),

    # Appointment
    path('device/appointment/', include('Appointment.APIs.device.urls') ),

    path('v1/doctor/', include('Doctor.APIs.v1.urls') ),
    path('device/doctor/', include('Doctor.APIs.v2.urls') ),
    path('doctor_dashboard/doctor/', include('Doctor.APIs.doctor_dashboard.urls') ),

    path('v1/hospital/', include('Hospital.APIs.v1.urls') ),
    path('v1/profile/', include('Profile.APIs.v1.urls') ),
    path('v1/meet/', include('Meet.urls') ),


    path('v1/product/', include('Product.API.urls') ),

    path('v1/pharmacy/', include('Pharmacy.API.v1.urls') ),
] 