
from django.urls import path



from .views import BookAppointmentPage, CheckoutPage


urlpatterns = [
    path('book-appointment', BookAppointmentPage, name='BookAppointmentPage'),
    path('checkout/', CheckoutPage, name='CheckoutPage'),

] 
