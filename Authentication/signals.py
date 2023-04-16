


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
    first_name, *last_name = user_name.split(' ')

    if len(last_name) > 0:
        last_name = last_name[0]
    else:
        last_name = ''

    user_profile = Profile(
        user = instance,
        first_name = first_name,
        last_name = last_name,
        full_name = instance.username,
        email = instance.email,
    )
    user_profile.is_selected = True
    user_profile.save()
    

@receiver(post_save, sender=User)
def user_created_signal__CreateUserProfile(sender, instance, created, **kwargs):
    if created:
        from Trauma.models import VerificationCode
        otp = VerificationCode.objects.create(
            user = instance
        )
        sendOtpEmail(
            {
                'user' : instance,
                'verification_code' : otp
            }
        )

    return
