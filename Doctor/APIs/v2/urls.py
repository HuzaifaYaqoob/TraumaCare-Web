



from django.urls import path

from Doctor.APIs.v2 import views as api_device

urlpatterns = [

    path('get-home-page-doctors/', api_device.getHomePageDoctors),
    path('get-doctor/<str:doctorId>/', api_device.getDoctorProfile),
    path('get-doctor-hospital-days/<str:hospitalId>/', api_device.getDoctorHospitalDays),
    path('get-doctor-hospital-slots/<str:doctorId>/<str:hospitalId>/', api_device.getDoctorHospitalSlots),
    path('book-appointment/<str:doctorId>/', api_device.BookAppointment_DoctorPage),
] 