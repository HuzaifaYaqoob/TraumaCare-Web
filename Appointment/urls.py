
from django.urls import path



from .views import BookAppointmentPage


urlpatterns = [
    path('book-appointment', BookAppointmentPage, name='BookAppointmentPage'),

] 