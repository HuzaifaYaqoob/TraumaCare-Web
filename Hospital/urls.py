
from django.urls import path


from . import views as hospital_views

urlpatterns = [
    path('search/', hospital_views.HospitalSearchPage, name='HospitalSearchPage'),
    path('<str:hospital_id>/', hospital_views.ViewHospitalProfile, name='ViewHospitalProfile')
] 