
from django import template

from Appointment.models import Appointment

register = template.Library()

@register.simple_tag(name='get_doctor_slots')
def get_doctor_slots(doctor, date, hospital_id):
    apps = Appointment.objects.filter(
        doctor__id = doctor.id,
        date = date,
        doct_hospital__id = hospital_id,
    ).exclude(
        status__in = ["Finished", "Cancelled"]
    ).values_list('start_time', flat=True)
    return [sTime.strftime('%H:%M:00') for sTime in apps]