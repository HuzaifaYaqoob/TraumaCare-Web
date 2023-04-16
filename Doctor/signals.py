

from django.db.models.signals import post_save
from django.dispatch import receiver

from Profile.models import Profile
from .models import Doctor, DoctorMedia


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