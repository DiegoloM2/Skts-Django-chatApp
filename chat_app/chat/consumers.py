"""
File of consumers to serve WebSockets
"""
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer): 
    def connect(self): #method run when socket is connected
        self.accept()
    
    def disconnect(self, close_code):
        pass

    def receive(self, text_data): 
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data = json.dumps({ #echoe message back to the sender
            'message': message
        }))