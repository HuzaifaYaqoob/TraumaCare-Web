

from Administration.models import SmsServiceKey
from Administration.Constant.Sms import generateSmsKey

def refreshSmsKey():
    tel_key = SmsServiceKey.objects.get_or_create(key_provider = 'Telenor')[0]
    generateSmsKey()