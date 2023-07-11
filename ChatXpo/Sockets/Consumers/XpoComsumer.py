

import json
from channels.generic.websocket import WebsocketConsumer

class XpoConsumer(WebsocketConsumer):

    def connect(self):
        print('hello world')
        self.accept()

        connected_data = {
            'type' : 'CHATXPO_CONNECTED',
            'status' : 200,
            'response' : {
                'display_message' : 'There always be a Display message to display on Client side',
                'message' : 'There always be a message',
                'error_message' : 'There always be a Error message if have, Otherwise empty strig',
                'data' : {},
            }
        }
        self.send(json.dumps(connected_data))
    
    def receive(self, text_data=None, bytes_data=None):
        print('data received')
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