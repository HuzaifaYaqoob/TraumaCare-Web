

from django.urls import path

from Authentication.APIs.v1 import views as v1_apis

urlpatterns = [
    path('validate-unique-user/', v1_apis.vaidate_unique_user, name='vaidate_unique_user' )
] 