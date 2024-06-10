
from datetime import datetime

from Doctor.models import DoctorWithHospital, DoctorTimeSlots


def appointment_get_doctor_availability(
    appointmentDate=datetime.now().strftime('%Y-%m-%d'),
    doctor_id=None,
    hospital_id=None,
    messages=[],
    slotsCount=1,
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
            slots_string_2 = slots_string_2 + f'{slot_intervals[0]} ({slot_intervals[1]}), '
    

    messages.append({'role' : 'system', 'content' : slots_string})
    messages.append({'role' : 'system', 'content' : slots_string_2})

    from ChatXpo.Sockets.Constant.Query import askChatXpo
    response = askChatXpo(
        'Re organize slots in Professional Way and then return slots',
        previousQueries=messages,
        onlyText=True
    )

    return response