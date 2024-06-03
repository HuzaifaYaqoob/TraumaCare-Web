from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital
from Appointment.models import Appointment, AppointmentGroup

from datetime import timedelta, datetime

# Create your views here.


def BookAppointmentPage(request):
    return render(request, 'Appointment/book_appointment.html')


def BookAppointment_DoctorPage(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid Request')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    doctor_id = request.POST.get('doctor', None)
    slot_id = request.POST.get('dr-appointment-slot', None)
    doct_hospital_id = request.POST.get('doct_hospital', None)

    selected_date = request.POST.get('selected_date', None)
    selected_time = request.POST.get('selected_time', None)

    try:
        doctor = Doctor.objects.get(id = doctor_id, is_deleted = False, is_blocked = False)
    except:
        messages.error(request, 'Invalid Doctor Profile')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if not doctor.is_active:
        messages.error(request, 'Doctor is not active')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    try:
        doct_hospital = DoctorWithHospital.objects.get(id = doct_hospital_id)
    except:
        messages.error(request, 'Doctor is not available at this Hospital.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        selected_slot = DoctorTimeSlots.objects.get(id = slot_id)
    except:
        messages.error(request, 'Selected Slot is not Available')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    appt_grp = AppointmentGroup.objects.create(
        user = request.user,
    )

    s_t = datetime.strptime(selected_time, "%H:%M:00")
    end_time = timedelta(minutes=20)
    end_time = end_time + s_t
    appointment = Appointment.objects.create(
        appointment_group = appt_grp,
        doctor = doctor,
        name = '',
        date = selected_date,
        start_time = selected_time,
        end_time=end_time.strftime("%H:%M"),
        slot = selected_slot,
        fee = selected_slot.fee,
        discount = selected_slot.discount,
        service_fee = selected_slot.service_fee,
        bill = selected_slot.final_price,
        status = 'Booked',
        appointment_location = 'InPerson',
        doct_hospital = doct_hospital
    )

    messages.success(request, 'Your appointment is booked successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def CheckoutPage(request):
    return render(request, 'checkout/checkout-appoinment.html')
