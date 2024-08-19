



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

from Administration.Constant.Sms import sendMessage, generateSmsKey

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.sessions_id = '88c9a5989f074452b1bd08c873780e84'
        super().__init__(*args, **kwargs)


    def send_message(self, numbers=[]):
        text = "Your TraumaCare verification code is 858150. Don't share this code with anyone. Thanks for choosing TraumaCare, an innovative healthcare solution by RedExpo."
        to = ''
        for num in numbers:
            to = to + str(num) + ','
        
        url = f'https://telenorcsms.com.pk:27677/corporate_sms2/api/sendsms.jsp?session_id={self.sessions_id}&to={to}&text={text}&mask=REDEXPO'
        print(url)
        response = requests.get(url)
        response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
        print(response_json)


    def handle(self, *args, **options):

        key = generateSmsKey()
        print(key)
        
        # self.send_message(
        #     numbers=["923400193324"]
        # )
       
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))


# 03bf20e39ccd41a49545f166cdaa56df