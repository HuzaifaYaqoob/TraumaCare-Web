
from datetime import datetime, timedelta

from Doctor.models import DoctorWithHospital, DoctorTimeSlots, Doctor
from Appointment.models import Appointment, AppointmentGroup


def appointment_get_doctor_availability(
    appointmentDate=datetime.now().strftime('%Y-%m-%d'),
    doctor_id=None,
    hospital_id=None,
    messages=[],
    slotsCount=1,
    **kwargs
):

    if not doctor_id or not hospital_id:
        return 'Please provide doctor_id or hospital_id'
    
    day_name = datetime.strptime(appointmentDate, '%Y-%m-%d').strftime('%A')

    doctor_hospitals = DoctorWithHospital.objects.filter(hospital__id=hospital_id, doctor__id = doctor_id)
    slots = DoctorTimeSlots.objects.filter(
        doc_hospital__in = doctor_hospitals, 
        is_deleted=False, 
        is_active=True,
        day__day__iexact = day_name
    ).order_by('start_time')

    slots_string = 'Doctor is available in following slots'
    slots_string_2 = 'Slots are : '
    for slot in slots:
        slot_intervals = slot.slots_interval
        if slot_intervals and len(slot_intervals) > 0:
            already_apps = Appointment.objects.filter(
                doctor__id = doctor_id,
                date = appointmentDate,
                doct_hospital = slot.doc_hospital,
            ).exclude(
                status__in = ["Finished", "Cancelled"]
            ).values_list('start_time', flat=True)
            already_apps = [sTime.strftime('%H:%M:00') for sTime in already_apps]
            print(already_apps)
            for inner_slot in slot_intervals:
                print(inner_slot[0])
                if inner_slot[0] in already_apps:
                    continue
                else:
                    slots_string_2 = slots_string_2 + f'Doctor available at {slot.doc_hospital.hospital.name} (Location : {slot.doc_hospital.location.uuid}, Location ID : {slot.doc_hospital.location.name}) {inner_slot[0]} ({inner_slot[1]}), '
    

    messages.append({'role' : 'system', 'content' : slots_string})
    messages.append({'role' : 'system', 'content' : slots_string_2})

    from ChatXpo.Sockets.Constant.Query import askChatXpo
    response = askChatXpo(
        'Re organize slots in Professional Way and then return slots along with location',
        previousQueries=messages,
        onlyText=True
    )

    return response


def book_user_appointment(
    appointmentDate=datetime.now().strftime('%Y-%m-%d'),
    doctor_id=None,
    hospital_id=None,
    location_id=None,
    selected_time=None,
    messages=[],
    user = None,
    **kwargs
):
    print(
        appointmentDate, \
        doctor_id, \
        hospital_id, \
        location_id, \
        selected_time, \
        user, \
)

    if user is None:
        return 'Please login to proceed <a href="/auth/login/">Login</a>'

    try:
        doctor = Doctor.objects.get(id = doctor_id, is_deleted = False, is_blocked = False)
    except Exception as err:
        print(err)
        return 'Invalid Doctor Profile'

    doct_hospital = DoctorWithHospital.objects.filter(
        hospital__id = hospital_id,
        doctor = doctor,
        location__id = location_id
    ).last()
    if not doct_hospital:
        return 'Doctor is not available at this Hospital.'
    

    selected_date = datetime.strptime(appointmentDate, "%Y-%m-%d")

    selected_slot = DoctorTimeSlots.objects.filter(
        doctor = doctor,
        doc_hospital = doct_hospital,
        day__day = selected_date.strftime('%A'),
        start_time__lte = selected_time,
        end_time__gte = selected_time,
        availability_type = 'Hospital',
        is_deleted = False,
        is_active = True
    ).last()
    if not selected_slot:
        return 'Not available in this slot.'
    
    appt_grp = AppointmentGroup.objects.create(
        user = user,
    )

    s_t = datetime.strptime(selected_time, "%H:%M:00")
    end_time = timedelta(minutes=doctor.get_time_inverval)
    end_time = end_time + s_t
    appointment = Appointment.objects.create(
        appointment_group = appt_grp,
        doctor = doctor,
        name = f'Appointment with {doctor.name} at {f"{doct_hospital.hospital.name}, {doct_hospital.location.name}" if hospital_id else "Online"}',
        date = selected_date.strftime("%Y-%m-%d"),
        start_time = selected_time,
        end_time=end_time.strftime("%H:%M"),
        slot = selected_slot,
        fee = selected_slot.fee,
        discount = selected_slot.discount,
        service_fee = selected_slot.service_fee,
        bill = selected_slot.final_price,
        status = 'Booked',
        appointment_location = 'InPerson' if hospital_id else 'Online',
    )
    if hospital_id:
        appointment.doct_hospital = doct_hospital
        appointment.save()
    from ChatXpo.Sockets.Constant.Query import askChatXpo

    return askChatXpo('Appointment is booked successfully, Kindly generate a professional message', previousQueries=messages, onlyText=True)