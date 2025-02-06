
from openai import OpenAI

from ChatXpo.GPTFunctionsCall.index import *
from ChatXpo.GPTFunctionsCall.FunctionsList import GPT_COMMON_FUNCTIONS

from Secure.models import XpoKey, ChatInstructions
import re

from Doctor.models import Doctor
from Hospital.models import Hospital




import json
from .Funcs import getUserOutput, getUserOutput_urdu

import re

def convert_to_html(content):
    """
    Converts ChatGPT special symbols to HTML content.
    
    Parameters:
    content (str): The input string containing ChatGPT special symbols.
    
    Returns:
    str: The converted HTML content.
    """
    
    # Replace '**' for bold text
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    
    # Replace '*' or '_' for italic text
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    content = re.sub(r'\_(.*?)\_', r'<em>\1</em>', content)
    
    # Replace '~~' for strikethrough text
    content = re.sub(r'\~\~(.*?)\~\~', r'<del>\1</del>', content)
    
    # Replace '`' for inline code
    content = re.sub(r'\`(.*?)\`', r'<code>\1</code>', content)
    
    # Replace links
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
    
    # Replace '\n' for new lines
    content = content.replace('\n', '<br>')
    
    # Handle nested Markdown (bold and italic together)
    content = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', content)
    
    # Handle bullet points (unordered lists)
    content = re.sub(r'^\s*-\s+(.*)', r'<li>\1</li>', content, flags=re.MULTILINE)
    if '<li>' in content:
        content = '<ul>' + content + '</ul>'
        content = content.replace('<ul><br>', '<ul>')
        content = content.replace('<br></li>', '</li>')
    
    return content



def askChatXpo(user_query, previousQueries=[], instructions=True, onlyText=False, user=None, inputFunction=None):
    key = XpoKey.objects.filter(is_active=True, is_deleted=False).order_by('-token_used')[0]
    client = OpenAI(api_key=key.key)
    # sk-a214fafd468e48639e937bbe46e7e4c1
    queries = [] or previousQueries

    my_query = {
        'role' : 'user',
        'content' : user_query
    }
    queries.append(my_query)

    INSTRUCTIONS = []
    if instructions:
        INSTRUCTIONS = [{'role' : 'system', 'content' : i.instruction} for i in ChatInstructions.objects.filter(is_active=True).order_by('-created_at')]
        doctors = Doctor.objects.filter(is_active=True, is_deleted=False).values('id', 'name', 'heading', 'slug')
        doctors_string = 'Available doctors on Traumacare Platform are : '
        for d in doctors:
            doctors_string += f'{d["name"]} (ID : {str(d["id"])}, slug: [{d["slug"]}]) & Speciality ({d["heading"]}), '

        hospitals = Hospital.objects.filter(is_active=True, is_deleted=False, is_blocked=False).values('id', 'name')
        hospitals_string = 'Available Hospitals on Traumacare Platform are : '
        for h in hospitals:
            hospitals_string += f'{h["name"]} ({h["id"]}), '
        
        INSTRUCTIONS.append({'role' : 'system', 'content' : doctors_string})
        INSTRUCTIONS.append({'role' : 'system', 'content' : hospitals_string})
        if user:
            INSTRUCTIONS.append({'role' : 'system', 'content' : f'User : {user.full_name}, Phone : {user.mobile_number}'})

    query = {}
    if not onlyText:
        query['functions'] = GPT_COMMON_FUNCTIONS
        query['function_call'] = 'auto'


    # Asking GPT 
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
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
        params = json.loads(choice.message.function_call.arguments)
        function_name = choice.message.function_call.name
        print(f'{function_name} function')
        choosen_function = eval(function_name)
        return choosen_function(**params, messages=queries, user=user)
    else:
        chat_message = response.choices[0].message
        return convert_to_html(chat_message.content)