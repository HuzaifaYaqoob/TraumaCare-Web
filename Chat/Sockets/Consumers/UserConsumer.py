

from channels.generic.websocket import WebsocketConsumer

class UserConsumer_Socket(WebsocketConsumer):

    def connect(self):
        return self.accept()