



from django.urls import path

from Doctor.APIs.doctor_dashboard import views as doctor_dashboard_apis

urlpatterns = [
    path('get-doctor/<str:doctorId>/', doctor_dashboard_apis.getDoctorProfile),
    path('get-doctor-appointments/', doctor_dashboard_apis.getDoctorAppointments),


    path('get-doctor-patients-for-dropdown/', doctor_dashboard_apis.getDoctorPatientsForDropdown),

    path('get-home-page-doctors/', doctor_dashboard_apis.getHomePageDoctors),
    path('get-doctor-hospital-days/<str:hospitalId>/', doctor_dashboard_apis.getDoctorHospitalDays),
    path('get-doctor-hospital-slots/<str:doctorId>/<str:hospitalId>/', doctor_dashboard_apis.getDoctorHospitalSlots),
    path('book-appointment/<str:doctorId>/', doctor_dashboard_apis.BookAppointment_DoctorPage),
] 