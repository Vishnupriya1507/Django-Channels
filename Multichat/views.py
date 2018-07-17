from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from chat.models import Room
from django.utils.safestring import mark_safe
import json

def main(request):
    return HttpResponseRedirect("/accounts/login/")

def logout(request):
    return HttpResponseRedirect("/chat/logout/")

def create_room(request):
    room_name = Room()
    room_name.save()
    print(type(room_name))
    return HttpResponse("heyyy")
    #return HttpResponseRedirect('/')
    #return render(request, 'chat/room.html', {'room_name_json': mark_safe(json.dumps(room_name)),'room_status':room_name.room_status})
    #'prob':prob,'users':users,