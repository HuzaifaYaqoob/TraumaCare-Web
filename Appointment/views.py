from django.shortcuts import render

# Create your views here.


def BookAppointmentPage(request):
    return render(request, 'Appointment/book_appointment.html')

def CheckoutPage(request):
    return render(request, 'checkout/checkout-appoinment.html')
