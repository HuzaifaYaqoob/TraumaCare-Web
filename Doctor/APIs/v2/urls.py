



from django.urls import path

from Doctor.APIs.v2 import views as api_device

urlpatterns = [

    path('get-home-page-doctors/', api_device.getHomePageDoctors),
    path('get-doctor/<str:doctorId>/', api_device.getDoctorProfile),
] 