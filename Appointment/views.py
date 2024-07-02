from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital
from Appointment.models import Appointment, AppointmentGroup
from Trauma.models import Speciality

from datetime import timedelta, datetime
from django.db.models import Count

# Create your views here.


def MyAppointmentsPage(request):
    today = datetime.now()
    appointments = Appointment.objects.filter(
            appointment_group__user = request.user,
            # date__gte = today.date()
        ).order_by('-date')
    
    data = { }
    for appt in appointments:
        print(appt.date.strftime('%B'))
        data[appt.date.strftime('%B')] = data.get(appt.date.strftime('%B')) or []
        data[appt.date.strftime('%B')].append(appt)
    context = {
        'appointments' : data
    }
    return render(request, 'Appointment/myAppointments.html', context)

def BookAppointmentPage(request):
    doctor_id = request.GET.get('doctor', None)
    context = {}
    if doctor_id:
        context['hospitals'] = DoctorWithHospital.objects.filter(doctor__id = doctor_id)
        
    
    context['today_label'] = datetime.now().strftime("%B %Y")
    context['doctors'] = Doctor.objects.filter(is_deleted = False, is_blocked = False, is_active = True)
    context['specialities'] = Speciality.objects.annotate(doctor_count=Count('speciality_doctorspecialities')).filter(is_deleted = False, is_active = True, doctor_count__gt = 0)
    
    return render(request, 'Appointment/book_appointment.html', context)


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
    
    if doct_hospital_id:
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
    end_time = timedelta(minutes=doctor.get_time_inverval)
    end_time = end_time + s_t
    appointment = Appointment.objects.create(
        appointment_group = appt_grp,
        doctor = doctor,
        name = f'Appointment with {doctor.name} at {f"{doct_hospital.hospital.name}, {doct_hospital.location.name}" if doct_hospital_id else "Online"}',
        date = selected_date,
        start_time = selected_time,
        end_time=end_time.strftime("%H:%M"),
        slot = selected_slot,
        fee = selected_slot.fee,
        discount = selected_slot.discount,
        service_fee = selected_slot.service_fee,
        bill = selected_slot.final_price,
        status = 'Booked',
        appointment_location = 'InPerson' if doct_hospital_id else 'Online',
    )
    if doct_hospital_id:
        appointment.doct_hospital = doct_hospital
        appointment.save()

    messages.success(request, 'Your appointment is booked successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def CheckoutPage(request):
    return render(request, 'checkout/checkout-appoinment.html')
