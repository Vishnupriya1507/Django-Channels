from django.shortcuts import render,HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db.utils import IntegrityError
from . models import Room,Problem
import json

def index(request):
    return render(request, 'chat/index.html', {})
    #return render(request, 'chat/create_new.html', {})


def room(request, room_name):
    
    #room = Room.objects.create(title = room_name)
    print(room_name)    
    return render(request, 'chat/room.html',{'room_name_json':mark_safe(json.dumps(room_name))})    ###mark_safe(json.dumps(room_name))



def create_room(request):
    #room = Room.objects.create(title = room_name)

    return HttpResponseRedirect('/chat/room_name')
   

    
    
    
        

