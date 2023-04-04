
from django.urls import path, include

urlpatterns = [

    path('', include('Trauma.APIs.v1.urls') ),
    path('v1/auth/', include('Authentication.APIs.v1.urls') ),
] 