

from django.db.models.signals import post_save
from django.dispatch import receiver

from Profile.models import Profile
from .models import Doctor, DoctorMedia, DoctorWithHospital
from Administration.models import PhoneMessage


@receiver(post_save, sender=Doctor)
def change_doctor_profiles_details(sender, instance, created, **kwargs):
    doc_profile = instance.profile

    doc_profile.full_name = instance.name
    doc_profile.email = instance.email

    doc_profile.save()


@receiver(post_save, sender=DoctorMedia)
def change_doctor_profiles_details_imgs(sender, instance, created, **kwargs):
    if instance.file_type != 'Profile Image':
        return
    
    doc_profile = instance.doctor.profile
    doc_profile.profile_image = instance.file
    doc_profile.save()


@receiver(post_save, sender=DoctorWithHospital)
def sendMessageToHospital_DoctorWithHospital(sender, instance, created, **kwargs):
    if not instance.is_hospital_informed:
        PhoneMessage.objects.create(
            phone_number = instance.phone,
            text = f"Dr. {instance.doctor.name} is now affiliated with {instance.hospital.name} ({instance.location.name}) and is open for patient appointments through TraumaCare, powered by RedExpo.",
            sms_type = 'DoctorWithHospital',
        )
        instance.is_hospital_informed = True
        instance.save()