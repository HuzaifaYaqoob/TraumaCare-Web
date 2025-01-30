


from django.db.models.signals import post_save
from django.dispatch import receiver

from Administration.models import PhoneMessage

from Administration.Constant.Sms import sendMessage

@receiver(post_save, sender=PhoneMessage)
def send_message(sender, instance, created, **kwargs):
    if created and not instance.is_sent and instance.priority == 1:
        sendMessage(instance)
