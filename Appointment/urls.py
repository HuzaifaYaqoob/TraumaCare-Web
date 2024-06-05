
from django.urls import path



from . import views as apptView


urlpatterns = [
    path('my-appointments', apptView.MyAppointmentsPage, name='MyAppointmentsPage'),
    path('book-appointment', apptView.BookAppointmentPage, name='BookAppointmentPage'),
    path('checkout/', apptView.CheckoutPage, name='CheckoutPage'),

    path('book-instant-appointment', apptView.BookAppointment_DoctorPage, name='BookAppointment_DoctorPage'),

] 
