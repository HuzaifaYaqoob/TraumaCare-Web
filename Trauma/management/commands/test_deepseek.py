



from django.core.management.base import BaseCommand

import csv
from django.conf import settings
from datetime import datetime
import time
import re
import random

import ollama
from ChatXpo.Sockets.Constant.Query import askChatXpo
from ChatXpo.GPTFunctionsCall.FunctionsList import GPT_COMMON_FUNCTIONS



class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        start_time = time.time()
        # data = ollama.list()
        # print(datsa)
        response = ollama.chat(
            model="deepseek-r1",
            messages=[
                # {"role": "user", "content": "My Name is Huzaifa Yaqoob"},
                {"role": "user", "content": "What are benifits of panadol?"},
            ],
            # stream=True,
            # tools = GPT_COMMON_FUNCTIONS,
        )
        
        

        # for index, chunk in enumerate(response):
        #     if index == 0:
        #         started_time = time.time()
        #         print('*'*50)
        #         print(f"Time taken: {round(started_time - start_time, 2)} seconds")
        #         print('*'*50)
        #     print(chunk['message']['content'], end='', flush=True)
        
        # print(response)
        end_time = time.time()
        print(f"Time taken: {round(end_time - start_time, 2)} seconds")
        print(response["message"]["content"])
        self.stdout.write(self.style.SUCCESS('Successfully added'))