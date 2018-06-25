from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.utils import IntegrityError
from . models import Room
import json

def index(request):
    return render(request, 'chat/index.html', {})
    #return render(request, 'chat/create_new.html', {})


def room(request, room_name):
    
   
        room = Room.objects.create(title = room_name)

        return render(request, 'chat/room.html',{'room_name_json': mark_safe(json.dumps(room_name))})



def create_room(request):
    room = Room()
    room.title = "bdcbd"
    room.save()
    return HttpResponseRedirect('/')

    
    
    
        

