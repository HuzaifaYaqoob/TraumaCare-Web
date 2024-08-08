



from django.core.management.base import BaseCommand

import csv
from django.conf import settings
from PIL import Image

from ChatXpo.Sockets.Constant.Query import askChatXpo

from datetime import datetime
import time

from openai import OpenAI

import re


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        file_path = 'Files/WhatsApp Image 2024-08-02 at 16.13.06.jpeg'

        import pytesseract
        from PIL import Image

        # Open the image file
        image = Image.open(file_path)

        # Perform OCR using PyTesseract
        text = pytesseract.image_to_string(image)

        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Print the extracted text
        print(text)


        # client = OpenAI(api_key='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')

        # queries = [ {"role": "system", "content": "You are a helpful assistant that can read images."}, 
        #            {"role": "user", "content": f"Extract the text from the image from "} ]

        # response = client.chat.completions.create(
        #     model = 'gpt-4-vision-preview',
        #     messages = queries,
        # )
        # choice = response.choices[0]
        # chat_message = response.choices[0].message
        # print(chat_message)




        self.stdout.write(self.style.SUCCESS('Successfully added Specialities'))

