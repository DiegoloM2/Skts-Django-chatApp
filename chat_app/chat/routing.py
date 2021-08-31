from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()), #regular expression path to 
                                                                                #serve socket connections to url: 
                                                                                    #ws/chat/<room-name>/
]