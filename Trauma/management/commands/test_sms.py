



from django.core.management.base import BaseCommand

import csv

from Blog.Cronjob import generateBlogPost
from Blog.models import BlogPostTopic, BlogMedia
from django.conf import settings
from PIL import Image
import requests

from datetime import datetime
from xml.etree import ElementTree
import time
import json
import xmltodict


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.sessions_id = '19b6f14ad95a4259ba18cf83acc74f89'
        super().__init__(*args, **kwargs)

    def get_session_id(self):
        url = 'https://telenorcsms.com.pk:27677/corporate_sms2/api/auth.jsp?msisdn=923400193324&password=BrightFuture098765'

        response = requests.post(url)
        response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
        print(response_json)
    

    def send_message(self, numbers=[]):
        text = 'Hello'
        to = '923187834096,923187130480'
        # for num in numbers:
        #     to = to + str(num) + ','
        
        url = f'https://telenorcsms.com.pk:27677/corporate_sms2/api/sendsms.jsp?session_id={self.sessions_id}&to={to}&text={text}&'
        print(url)
        response = requests.get(url)
        response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
        print(response_json)


    def handle(self, *args, **options):

        # self.get_session_id()
        
        self.send_message(
            numbers=['923464529005',]
        )
       
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))


# 03bf20e39ccd41a49545f166cdaa56df