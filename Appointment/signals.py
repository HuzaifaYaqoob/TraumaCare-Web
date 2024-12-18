

from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Appointment
from Administration.models import PhoneMessage

@receiver(post_save, sender=Appointment)
def generatePhoneMessage_Appointment(sender, instance, created, **kwargs):
    if not instance.is_sms_sent:

        if type(instance.date) == str:
            app_date = instance.date
            app_time = instance.start_time
        else:
            app_date = instance.date.strftime('%B %d, %Y')
            app_time = instance.start_time.strftime('%I:%M %p')

        patient = instance.appointment_group.user
        doctor = instance.doctor

        if instance.appointment_location == 'Online':
            to = f"{patient.mobile_number},{doctor.user.mobile_number}"
            PhoneMessage.objects.create(
                phone_number = to,
                sms_type = 'OnlineAppointment',
                text = f"Online appointment confirmed: {patient.full_name} has an online appointment with Dr. {doctor.name} on {app_date} at {app_time}, booked via TraumaCare, powered by RedExpo."
            )

        elif instance.appointment_location == 'InPerson' and instance.doct_hospital:
            hospital = instance.doct_hospital.hospital
            location = instance.doct_hospital.location

            to = f'{patient.mobile_number},{doctor.user.mobile_number},{instance.doct_hospital.phone}'
            PhoneMessage.objects.create(
                phone_number = to,
                sms_type = 'Appointment',
                text = f"Appointment Confirmation: {patient.full_name} has an appointment with Dr. {doctor.name} at {hospital.name}, {location.name}, on {app_date} at {app_time}. Confirmed via TraumaCare, powered by RedExpo."
            )

        instance.is_sms_sent = True
        instance.save()
