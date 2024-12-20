
from django.db.models.signals import post_save
from django.dispatch import receiver

from Profile.models import Profile
from Doctor.models import Doctor
from Hospital.models import Hospital
from django.conf import settings

@receiver(post_save, sender=Profile)
def createDoctorOrHospital(sender, instance, created, **kwargs):
    if created:
        if instance.profile_type == 'Doctor':
            Doctor.objects.create(
                user = instance.user,
                profile = instance,
                email = instance.user.email,
                name = instance.full_name,
                # heading
                # dial_code
                mobile_number = instance.user.mobile_number,
                # working_since
                # online_availability
                # desc
                # slug
                # is_approved
                # is_active
                # is_deleted
                # is_blocked
                # is_featured
                # is_recommended
            )
        elif instance.profile_type == 'Hospital':
            Hospital.objects.create(
                user = instance.user,
                profile = instance,
                # facility_type = 'Hospital',
                name = instance.full_name,
                # description
                # slug
                fee = settings.TRAUMACARE_FEE,
                # is_approved
                # is_onboard
                # is_active
                # is_deleted
                # is_blocked
                # is_featured
                # is_recommended
            )