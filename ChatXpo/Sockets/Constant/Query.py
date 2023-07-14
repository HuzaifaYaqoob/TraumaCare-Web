
import openai

from Secure.models import XpoKey
from .Instructions import INSTRUCTIONS
import re


key = XpoKey.objects.all()[0]
openai.api_key = key.key
connection = openai.ChatCompletion()

import json
from .Funcs import getUserOutput, getUserOutput_urdu

def askChatXpo(user_query, previousQueries=[]):
    queries = [] + previousQueries
    queries.append(INSTRUCTIONS)

    my_query = {
        'role' : 'user',
        'content' : user_query
    }
    queries.append(my_query)

    # Asking GPT 
    response = connection.create(model = 'gpt-3.5-turbo', messages=queries)
    answer = response.choices[0].message.content
    answer = answer.replace(': ', ':')


    content = response
    extracted_info = answer

    user_output = getUserOutput(answer)

    user_translation = getUserOutput_urdu(answer)
    if not user_translation:
        from googletrans import Translator
        translator = Translator()
        user_translation = translator.translate(user_output, dest='ur').text

    return {
        'content' : content,
        'user_output' : user_output,
        'extracted_info' : extracted_info,
        'user_output_urdu_translation' : user_translation
    }
