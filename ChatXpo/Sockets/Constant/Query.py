
from openai import OpenAI

from ChatXpo.GPTFunctionsCall.index import *
from ChatXpo.GPTFunctionsCall.FunctionsList import GPT_COMMON_FUNCTIONS

from Secure.models import XpoKey, ChatInstructions
import re

from Doctor.models import Doctor
from Hospital.models import Hospital




import json
from .Funcs import getUserOutput, getUserOutput_urdu

def askChatXpo(user_query, previousQueries=[], instructions=True, onlyText=False):
    key = XpoKey.objects.filter(is_active=True, is_deleted=False).order_by('-token_used')[0]
    client = OpenAI(api_key=key.key)
    queries = [] or previousQueries

    my_query = {
        'role' : 'user',
        'content' : user_query
    }
    queries.append(my_query)

    INSTRUCTIONS = []
    if instructions:
        INSTRUCTIONS = [{'role' : 'system', 'content' : i.instruction} for i in ChatInstructions.objects.filter(is_active=True).order_by('-created_at')]
        doctors = Doctor.objects.filter(is_active=True, is_deleted=False).values('id', 'name')
        doctors_string = 'Available doctors on Traumacare Platform are : '
        for d in doctors:
            doctors_string += f'{d["name"]} ({d["id"]}), '

        hospitals = Hospital.objects.filter(is_active=True, is_deleted=False, is_blocked=False).values('id', 'name')
        hospitals_string = 'Available Hospitals on Traumacare Platform are : '
        for h in hospitals:
            hospitals_string += f'{h["name"]} ({h["id"]}), '
        
        INSTRUCTIONS.append({'role' : 'system', 'content' : doctors_string})
        INSTRUCTIONS.append({'role' : 'system', 'content' : hospitals_string})

    query = {}
    if not onlyText:
        query['functions'] = GPT_COMMON_FUNCTIONS
        query['function_call'] = 'auto'


    # Asking GPT 
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = INSTRUCTIONS + queries,
        **query
    )

    key.completion_tokens = key.completion_tokens + response.usage.completion_tokens
    key.prompt_tokens = key.prompt_tokens + response.usage.prompt_tokens
    key.token_used = key.token_used + response.usage.total_tokens
    key.total_requests = key.total_requests + 1
    key.save()

    choice = response.choices[0]

    if choice.finish_reason == 'function_call':
        print('function')
        params = json.loads(choice.message.function_call.arguments)
        function_name = choice.message.function_call.name
        choosen_function = eval(function_name)
        return choosen_function(**params, messages=queries)
    else:
        chat_message = response.choices[0].message
        return chat_message.content