


from django.db.models.signals import post_save
from django.dispatch import receiver

from Constants.Emails.OtpEmail import sendOtpEmail

from Authentication.models import User
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
    

# @receiver(post_save, sender=User)
# def user_created_signal__SendOTPEmail(sender, instance, created, **kwargs):
#     if created:
#         from Trauma.models import VerificationCode
#         otp = VerificationCode.objects.create(
#             user = instance
#         )
#         sendOtpEmail(
#             {
#                 'user' : instance,
#                 'verification_code' : otp
#             }
#         )

#     return


@receiver(post_save, sender=User)
def user_created_signal__CreateDRFToken(sender, instance, created, **kwargs):
    if created:
        from rest_framework.authtoken.models import Token 
        Token.objects.get_or_create(user = instance)

    return
