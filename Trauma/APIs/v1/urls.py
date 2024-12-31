
from django.urls import path, include

from . import views as v1Apis

urlpatterns = [

    path('get_all_specialities/', v1Apis.get_all_specialities),
    path('get_all_diseases/', v1Apis.get_all_diseases),
    path('get_speciality_doctors/<str:spaciality_slug>/', v1Apis.get_speciality_doctors),

] 