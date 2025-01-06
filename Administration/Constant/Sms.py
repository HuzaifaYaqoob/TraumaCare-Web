


from Administration.models import SmsServiceKey
import requests
import json
import xmltodict


def generateSmsKey():

    url = 'https://telenorcsms.com.pk:27677/corporate_sms2/api/auth.jsp?msisdn=923400193324&password=BrightFuture098765'

    response = requests.post(url)
    response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
    corpsms = response_json.get('corpsms', None)
    # {'corpsms': {'command': 'Auth_request', 'data': '88c9a5989f074452b1bd08c873780e84', 'response': 'OK'}}
    if not corpsms:
        return False

    status = corpsms.get('response', None)
    if status != 'OK':
        return


    api_key = corpsms.get('data', None)
    tel_key = SmsServiceKey.objects.get_or_create(key_provider = 'Telenor')[0]
    tel_key.key = api_key
    tel_key.save()

    return api_key

def sendMessage(sms_instance, provider='Telenor'):
    if not sms_instance.text or not sms_instance.phone_number:
        return
    
    phone_numbers = sms_instance.phone_number.split(',')
    final_numbers = []
    for phn in phone_numbers:
        if phn != '0000':
            final_numbers.append(phn)

    if len(final_numbers) == 0:
        sms_instance.is_deleted = True
        sms_instance.save()
        return
        
    final_numbers = ','.join(final_numbers)

    api_key = SmsServiceKey.objects.get_or_create(key_provider = provider)[0]

    url = f'https://telenorcsms.com.pk:27677/corporate_sms2/api/sendsms.jsp?session_id={api_key}&to={final_numbers}&text={sms_instance.text}&mask=REDEXPO'
    print(url)
    response = requests.get(url)
    response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
    # {'corpsms': {'command': 'Submit_SM', 'data': '5275753564', 'response': 'OK'}}
    corpsms = response_json.get('corpsms', None)
    if not corpsms:
        return False

    status = corpsms.get('response', None)
    if status != 'OK':
        return False
    
    messsageIds = corpsms.get('data', '')
    sms_instance.sms_ids = messsageIds
    sms_instance.is_sent = True
    sms_instance.save()

    return True
    print(response_json)