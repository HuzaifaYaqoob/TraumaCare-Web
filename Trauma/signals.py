

from .models import VerificationCode
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=VerificationCode)
def user_created_signal__SendOTPEmail(sender, instance, created, **kwargs):
    if created:
        VerificationCode.objects.filter(
            user = instance.user,
            otp_type = instance.otp_type,
        ).exclude(
            id = instance.id
        ).update(
            is_expired = True,
            is_deleted = True
        )