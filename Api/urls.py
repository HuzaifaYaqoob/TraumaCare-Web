
from django.urls import path, include

urlpatterns = [

    path('v1/auth/', include('Authentication.APIs.v1.urls') )
] 