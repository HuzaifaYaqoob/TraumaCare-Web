



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
        super().__init__(*args, **kwargs)

    def get_session_id(self):
        url = 'https://telenorcsms.com.pk:27677/corporate_sms2/api/auth.jsp?msisdn=923400193324&password=Dev123404'

        response = requests.get(url)
        response_json = json.loads(json.dumps(xmltodict.parse(response.content)))
        print(response_json)


    def handle(self, *args, **options):

        self.get_session_id()
       
        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

