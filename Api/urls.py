
from django.urls import path, include

urlpatterns = [

    path('', include('Trauma.APIs.v1.urls') ),
    path('v1/auth/', include('Authentication.APIs.v1.urls') ),
    path('v1/chatxpo/', include('ChatXpo.Apis.v1.urls') ),

    path('v1/doctor/', include('Doctor.APIs.v1.urls') ),
    path('device/doctor/', include('Doctor.APIs.v2.urls') ),

    path('v1/hospital/', include('Hospital.APIs.v1.urls') ),
    path('v1/profile/', include('Profile.APIs.v1.urls') ),
    path('v1/meet/', include('Meet.urls') ),
] 