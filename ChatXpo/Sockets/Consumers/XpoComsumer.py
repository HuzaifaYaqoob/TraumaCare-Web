

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from ChatXpo.models import ChatMessage, XpoChat
from Authentication.models import User
from ChatXpo.Apis.v1.serializers import ChatMessageSerializer
from ChatXpo.Sockets.Constant.index import SendAiGeneratedMessageToUser

class XpoConsumer(WebsocketConsumer):

    def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        try:
            user = User.objects.get(id = user_id)
        except:
            user = None
        
        if user is None:
            return
        self.user = user

        self.accept()

        self.room_group_name = f'chat-xpo-user-{user_id}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        connected_data = {
            'type' : 'CHATXPO_CONNECTED',
            'status' : 200,
            'response' : {
                'display_message' : 'Connected with Chat',
                'message' : 'Connected',
                'error_message' : '',
                'data' : {},
            }
        }
        self.send(json.dumps(connected_data))
    
    def onError(self, errorMessage):
        message_data = {
            'type' : 'CHATXPO_AI_GENERATED_ERROR',
            'status' : 500,
            'response' : {
                'display_message' : 'ERROR',
                'message' : 'ERROR',
                'error_message' : errorMessage,
                'data' : None
            }
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'send_message',
                'content' : message_data
            }
        )

    def UserNewQuestion(self, content):
        chatId = content.get('chatId', None)
        if chatId is None:
            return
        
        try:
            chat = XpoChat.objects.get(uuid = chatId)
        except Exception as err:
            notFound_data = {
                'type' : 'CHATXPO_CHAT_NOT_FOUND',
                'status' : 404,
                'response' : {
                    'display_message' : 'Chat Not Found',
                    'message' : 'Chat Not Found',
                    'error_message' : str(err),
                    'data' : {},
                }
            }
            self.send(json.dumps(notFound_data))
        else:
            chatMessage = content.get('message', None)
            newMessage = ChatMessage.objects.create(
                chat = chat,
                user_query = chatMessage,
                message_type = 'Message'
            )
            if not chat.title:
                chat.title = chatMessage
                chat.save()
                message_data = {
                    'type' : 'CHATXPO_CHAT_TITLE_UPDATED',
                    'status' : 200,
                    'response' : {
                        'display_message' : 'Chat Title Updated',
                        'message' : 'Chat Title Updated',
                        'error_message' : '',
                        'data' : {
                            'chatId' : f'{chat.uuid}',
                            'title' : chat.title
                        },
                    }
                }
                self.send(json.dumps(message_data))
            data = ChatMessageSerializer(newMessage).data
            message_data = {
                'type' : 'CHATXPO_NEW_CHAT_MESSAGE',
                'status' : 201,
                'response' : {
                    'display_message' : 'New Message',
                    'message' : 'New Message',
                    'error_message' : '',
                    'data' : {
                        'chatId' : f'{chat.uuid}',
                        'send_user_id' : f'{self.user.id}',
                        'message' : data
                    },
                }
            }
            self.send(json.dumps(message_data))
            SendAiGeneratedMessageToUser(chatMessage = newMessage, onError=self.onError)
            

    def send_message(self, event):
        content = event['content']
        self.send(text_data=json.dumps(content))
    
    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return super().receive(text_data, bytes_data)

        data = json.loads(text_data)
        messageType = data.get('type', None)
        if messageType is None:
            return
        
        content = data.get('content', {})
        if messageType == 'CHAT_NEW_MESSAGE':
            self.UserNewQuestion(content)

    
    def disconnect(self, code):
        print('disconnected from Frontend')
        return super().disconnect(code)


{
    'type' : 'TYPE_IN_UPPERCASE_LETTERS',
    'status' : 200,
    'response' : {
        'message' : 'There always be a message',
        'error_message' : 'There always be a Error message if have, Otherwise empty strig',
        'data' : {},
    }
}