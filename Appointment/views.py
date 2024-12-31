from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.contrib import messages

from Doctor.models import Doctor, DoctorTimeSlots, DoctorWithHospital
from Appointment.models import Appointment, AppointmentGroup
from Trauma.models import Speciality

from datetime import timedelta, datetime
from django.db.models import Count



def MyAppointmentsPage(request):
    today = datetime.now()
    req_status = request.GET.get('status', None)

    query = {}

    if not req_status or req_status == 'ALL':
        pass
    elif req_status == 'Upcoming':
        query['date__gte'] = today.date()
    elif req_status == 'Past':
        query['date__lt'] = today.date()
    elif req_status == 'Cancelled':
        query['status__in'] = ['Cancelled', 'Expired']
    else:
        query['status'] = req_status

    appointments = Appointment.objects.filter(
            appointment_group__user = request.user,
            **query
        ).order_by('-date')
    
    data = { }
    for appt in appointments:
        data[appt.date.strftime('%B')] = data.get(appt.date.strftime('%B')) or []
        data[appt.date.strftime('%B')].append(appt)
    context = {
        'appointments' : data
    }
    return render(request, 'Appointment/myAppointments.html', context)

def CancelMyAppointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id = appointment_id, appointment_group__user = request.user)
    except:
        messages.error(request, 'Invalid Request')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        appointment.status = 'Cancelled'
        appointment.appointment_group.status = 'Cancelled'
        appointment.appointment_group.save()
        appointment.save()
        messages.success(request, 'Appointment Cancelled')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def BookAppointmentPage(request):
    doctor_slug = request.GET.get('doctor', None)
    context = {}
    if doctor_slug:
        try:
            doctor = Doctor.objects.get(slug = doctor_slug)
        except:
            messages.error(request, 'Invalid Doctor profile')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            context['doctor'] = doctor
        
        hospital_id = request.GET.get('hospital', None)
        mode = request.GET.get('mode', None)
        hospital = None
        if mode == 'Online':
            context['mode'] = mode
            
        elif hospital_id :
            try:
                hospital = DoctorWithHospital.objects.get(id = hospital_id)
            except:
                messages.error(request, 'Invalid Hospital')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            context['hospital'] = hospital
        else:
            context['hospitals'] = DoctorWithHospital.objects.filter(doctor = doctor, hospital__is_deleted = False, hospital__is_active = True, hospital__is_blocked = False)
        
        if hospital or mode == 'Online':
            days_slots = []
            date_now = datetime.now()
            for i in range(30):
                date = date_now + timedelta(days = i)
                data = {
                    'date' : date,
                    'day_name' : date.strftime("%a"),
                    'date_format' : date.strftime("%Y-%m-%d"),
                    'date_prefix_zero' : date.strftime("%d"),
                }
                if i == 0:
                    data['is_today'] = True
                else:
                    data['month'] = date.strftime("%B")
                days_slots.append(data)
            context['days_slots'] = days_slots
    else:
        speciality_get = request.GET.get('speciality', '')
        context['doctors'] = Doctor.objects.filter(is_deleted = False, is_blocked = False, is_active = True, doctor_specialities__speciality__slug = speciality_get)
    
    
    return render(request, 'Appointment/book_appointment.html', context)


def BookAppointment_DoctorPage(request):
    if request.method == 'GET':
        return render(request, 'checkout/checkout_appoinment.html')
    elif request.method == 'POST':
        
        print(request.POST)
        # doctor
        # selected_date
        # doct_hospital
        # dr-appointment-slot
        # selected_time

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
            doct_hospital = doct_hospital if doct_hospital_id else None,
        )

        messages.success(request, 'Your appointment is booked successfully.')
        return redirect(f'/appointment/my-appointments#appointment_{appointment.id}')

def CheckoutPage(request):
    return render(request, 'checkout/checkout-appoinment.html')
