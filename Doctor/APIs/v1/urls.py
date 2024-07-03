



from django.urls import path

from Doctor.APIs.v1 import views as api_v1

urlpatterns = [

    path('create-doctor-profile/', api_v1.createDoctorProfile),
    path('get_doctor_slots/<str:doctor_id>/<str:hospital_id>/', api_v1.getDoctorHospitalSlots),
] 