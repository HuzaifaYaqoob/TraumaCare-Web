

import time
from ChatXpo.Apis.v1.serializers import ChatMessageSerializer
from ChatXpo.models import ChatMessage
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .Query import askChatXpo

from Secure.models import XpoKey
key = XpoKey.objects.all()

if key:
    key = key[0].key
else:
    key = 'No key'

def sendError(error, user=None):
    message_data = {
        'type' : 'CHATXPO_AI_GENERATED_ERROR',
        'status' : 200,
        'response' : {
            'display_message' : 'ERROR',
            'message' : 'ERROR',
            'error_message' : error,
            'key' : str(key),
            'data' : None
        }
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat-xpo-user-{user.id}',
        {
            'type' : 'send_message',
            'content' : message_data
        }
    )

def getPreviousQueries(chat):
    queries = []
    previousChats = ChatMessage.objects.filter(
        chat = chat
    ).order_by('created_at')
    for chatMsg in previousChats:
        queries.append({
            'role' : 'user',
            'content' : chatMsg.user_query
        })
        queries.append({
            'role' : 'assistant',
            'content' : chatMsg.display_content
        })
    
    return queries

def SendAiGeneratedMessageToUser(chatMessage=None, onError=sendError):
    if chatMessage is None:
        onError('chatMessage is None', )
    
    try:
        chat = chatMessage.chat
        user = chat.user
        

        query_answer = askChatXpo(chatMessage.user_query, previousQueries=getPreviousQueries(chat))
        content = query_answer['content']
        user_output = query_answer['user_output']
        extracted_info = query_answer['extracted_info']
        user_output_urdu_translation = query_answer['user_output_urdu_translation']
        
        AI_Message = chatMessage
        AI_Message.content = content
        AI_Message.display_content = user_output
        AI_Message.extracted_info = extracted_info
        AI_Message.user_output_urdu = user_output_urdu_translation
        AI_Message.save()

        data = ChatMessageSerializer(AI_Message).data
        message_data = {
            'type' : 'CHATXPO_AI_GENERATED_CHAT_MESSAGE',
            'status' : 200,
            'response' : {
                'display_message' : 'Updated Message',
                'message' : 'Updated Message',
                'error_message' : '',
                'data' : {
                    'chatId' : f'{chat.uuid}',
                    'send_user_id' : f'{chat.user.id}',
                    'message' : data
                },
            }
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat-xpo-user-{user.id}',
            {
                'type' : 'send_message',
                'content' : message_data
            }
        )
    except Exception as err:
        onError(f'{str(err)} ---- {key}')