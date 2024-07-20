

from django.db.models.signals import post_save
from django.dispatch import receiver


from .models import Appointment
from Administration.models import PhoneMessage

@receiver(post_save, sender=Appointment)
def generatePhoneMessage_Appointment(sender, instance, created, **kwargs):
    if not instance.is_sms_sent:
        print()

        if type(instance.date) == str:
            app_date = instance.date
            app_time = instance.start_time
        else:
            app_date = instance.date.strftime('%B %d, %Y')
            app_time = instance.start_time.strftime('%I:%M %p')

        if instance.appointment_location == 'Online':

            # Send Message to Patient
            PhoneMessage.objects.create(
                phone_number = instance.appointment_group.user.mobile_number,
                sms_type = 'OnlineAppointment',
                text = f"Your online appointment with Dr. {instance.doctor.name} on {app_date} at {app_time} has been confirmed by TraumaCare, powered by RedExpo."
            )
            # Send Message to Doctor
            PhoneMessage.objects.create(
                phone_number = instance.doctor.user.mobile_number,
                sms_type = 'OnlineAppointment',
                text = f"You have a new online appointment with {instance.appointment_group.user.full_name} on {app_date} at {app_time}, booked via TraumaCare, powered by RedExpo."
            )
            instance.is_sms_sent = True
            instance.save()
        elif instance.appointment_location == 'InPerson' and instance.doct_hospital:
            hospital = instance.doct_hospital.hospital
            location = instance.doct_hospital.location
            # Send Message to Patient
            PhoneMessage.objects.create(
                phone_number = instance.appointment_group.user.mobile_number,
                sms_type = 'Appointment',
                text = f"Your appointment with Dr. {instance.doctor.name} at {hospital.name}, {location.name} on {app_date} at {app_time} has been confirmed by TraumaCare, powered by RedExpo."
            )
            # Send Message to Doctor
            PhoneMessage.objects.create(
                phone_number = instance.doctor.user.mobile_number,
                sms_type = 'Appointment',
                text = f"You have a new appointment with {instance.appointment_group.user.full_name} at {hospital.name}, {location.name} on {app_date} at {app_time}, booked via TraumaCare, powered by RedExpo."
            )
            # Send Message to Hospital
            PhoneMessage.objects.create(
                phone_number = instance.doct_hospital.phone,
                sms_type = 'Appointment',
                text = f"An appointment has been scheduled with Dr. {instance.doctor.name} on {app_date} at {app_time}. Patient: {instance.appointment_group.user.full_name}. Location: {hospital.name}, {location.name}. Confirmed via TraumaCare, powered by RedExpo."
            )
            instance.is_sms_sent = True
            instance.save()
