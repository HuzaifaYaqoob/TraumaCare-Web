
from channels.generic.websocket import WebsocketConsumer

class UserConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()

    
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)


    def disconnect(self, code):
        print('disconnected *******')