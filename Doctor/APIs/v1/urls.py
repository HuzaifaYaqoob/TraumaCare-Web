



from django.urls import path

from Doctor.APIs.v1 import views as api_v1

urlpatterns = [

    path('create-doctor-profile/', api_v1.createDoctorProfile),
] 