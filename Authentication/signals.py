


from django.db.models.signals import post_save
from django.dispatch import receiver

from Constants.Emails.OtpEmail import sendOtpEmail

from Authentication.models import User
from Trauma.models import VerificationCode
from Profile.models import Profile

@receiver(post_save, sender=User)
def user_created_signal__CreateUserProfile(sender, instance, created, **kwargs):
    if not created:
        return


    user_name = instance.username

    user_profile = Profile(
        user = instance,
        first_name = instance.first_name,
        last_name = instance.last_name,
        full_name = f'{instance.first_name} {instance.last_name}'.strip(),
        email = instance.email,
    )
    user_profile.is_selected = True
    user_profile.save()
    

@receiver(post_save, sender=VerificationCode)
def generatePhoneMessage_VerificationCode(sender, instance, created, **kwargs):
    if created and instance.otp_type == 'MOBILE_VERIFICATION':
        from Administration.models import PhoneMessage
        PhoneMessage.objects.create(
            phone_number = instance.mobile_number,
            sms_type = 'OTP',
            text = f"Your TraumaCare verification code is {instance.code}. Don't share this code with anyone. Thanks for choosing TraumaCare, an innovative healthcare solution by RedExpo."
        )


@receiver(post_save, sender=User)
def user_created_signal__CreateDRFToken(sender, instance, created, **kwargs):
    if created:
        from rest_framework.authtoken.models import Token 
        Token.objects.get_or_create(user = instance)

    return
