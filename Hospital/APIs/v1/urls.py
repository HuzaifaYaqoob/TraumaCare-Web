



from django.urls import path, include

from Hospital.APIs.v1 import views as hospitalViews


urlpatterns = [

    path('create-hospital-profile/', hospitalViews.createHospitalProfile),
] 