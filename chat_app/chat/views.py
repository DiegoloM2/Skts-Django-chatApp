from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required

def index(request): 
    return render(request, "chat/index.html")

@login_required #make login required
def room(request, room_name): 
    return render(request, "chat/room.html", {
        "room_name": mark_safe(json.dumps(room_name)), 
        "username": mark_safe(json.dumps(request.user.username))
    })