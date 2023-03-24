


from django.db.models.signals import post_save
from django.dispatch import receiver


from Authentication.models import User

@receiver(post_save, sender=User)
def user_created_signal__CreateUserProfile(sender, instance, created, **kwargs):
    if not created:
        return
    
    
    print('*****************')
    print('Create user signal callled user_created_signal__CreateUserProfile')
    print('created : ', created)
    print('instance : ', instance)
    print('*****************')