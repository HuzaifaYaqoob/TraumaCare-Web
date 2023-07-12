

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class XpoConsumer(WebsocketConsumer):

    def connect(self):
        user_id = self.scope['url_route']['kwargs']['user_id']
        print(user_id)
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
    

    def send_message(self, event):
        content = event['content']
        self.send(text_data=json.dumps(content))
    
    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return super().receive(text_data, bytes_data)

        data = json.loads(text_data)

        print('data received', data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type' : 'send_message', 'content' : data}
        )
        return super().receive(text_data, bytes_data)
    
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