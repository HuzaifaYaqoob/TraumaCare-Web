
from django.db.models.signals import post_save
from django.dispatch import receiver

from Profile.models import Profile
from Doctor.models import Doctor
from Hospital.models import Hospital
from Pharmacy.models import Store
from django.conf import settings

@receiver(post_save, sender=Profile)
def createDoctorOrHospital(sender, instance, created, **kwargs):
    if created:
        if instance.profile_type == 'Doctor':
            Doctor.objects.create(user = instance.user, profile = instance, name = instance.full_name, email = instance.user.email, mobile_number = instance.user.mobile_number,)
        elif instance.profile_type == 'Hospital':
            Hospital.objects.create(user = instance.user, profile = instance, name = instance.full_name, fee = settings.TRAUMACARE_FEE,)
        elif instance.profile_type == 'Pharmacy':
            Store.objects.create(user = instance.user, profile = instance, name = instance.full_name, phone = instance.user.mobile_number, email = instance.user.email,)