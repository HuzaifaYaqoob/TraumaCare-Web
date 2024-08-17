

from Administration.models import SmsServiceKey

def refreshSmsKey():
    tel_key = SmsServiceKey.objects.get_or_create(key_provider = 'Telenor')[0]

    return 'REDEXPO'