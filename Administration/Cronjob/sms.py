

from Administration.models import SmsServiceKey, PhoneMessage
from Administration.Constant.Sms import generateSmsKey, sendMessage

def refreshSmsKey():
    tel_key = SmsServiceKey.objects.get_or_create(key_provider = 'Telenor')[0]
    generateSmsKey()


def sendPendingSms():
    pending_sms = PhoneMessage.objects.filter(is_sent = False, is_deleted=False).order_by('priority')

    for sms in pending_sms:
        sendMessage(sms)