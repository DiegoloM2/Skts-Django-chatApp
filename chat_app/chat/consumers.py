import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404


User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_30_messages()
        serializer = MessageSerializer(messages, many = True)
        jsonSerializedMessages = JSONRenderer().render(serializer.data)
        content = {
            "messages":jsonSerializedMessages
        }

        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        user = get_object_or_404(User, username = author)
        message = Message.objects.create(author = user, content = data['message'])

        content = {
            'command':'new_message', 
            'message': message.content, 
            'author': author
        }

        return self.send_chat_message(content)

    commands = {
        'fetch_messages':fetch_messages, 
        'new_message':new_message
    }



    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        self.commands[command](self, data)
        # send_chat_message(message)


    def send_chat_message(self, data):



        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chatMessage', #this is the name 
                                        #of the callback function 
                                        #that then sends the message
                                        #to the websocket
                'data':data
            }
        )


    def send_message(self, message):
        self.send(text_data = json.dumps(message))

    # Receive message from room group
    def chatMessage(self, event):
        data = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))