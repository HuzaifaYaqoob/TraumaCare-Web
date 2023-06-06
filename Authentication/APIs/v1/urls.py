

from django.urls import path

from Authentication.APIs.v1 import views as v1_apis

urlpatterns = [
    path('validate-unique-user/', v1_apis.vaidate_unique_user, name='vaidate_unique_user' ),

    path('login/', v1_apis.Login ),
    path('signup/', v1_apis.Signup ),
] 