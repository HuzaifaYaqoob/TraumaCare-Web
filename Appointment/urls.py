
from django.urls import path



from . import views as apptView
# login required 
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('my-appointments', login_required(apptView.MyAppointmentsPage, login_url='/auth/login/'), name='MyAppointmentsPage'),
    path('my-appointments/cancel-appointment/<str:appointment_id>/', login_required(apptView.CancelMyAppointment, login_url='/auth/login/'), name='CancelMyAppointment'),
    path('book-appointment', login_required(apptView.BookAppointmentPage, login_url='/auth/login/'), name='BookAppointmentPage'),
    path('checkout/', login_required(apptView.CheckoutPage, login_url='/auth/login/'), name='CheckoutPage'),

    path('book-instant-appointment', login_required(apptView.BookAppointment_DoctorPage, login_url='/auth/login/'), name='BookAppointment_DoctorPage'),

] 
