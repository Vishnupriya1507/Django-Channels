from __future__ import unicode_literals
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.utils.safestring import mark_safe
from django.db.utils import IntegrityError
from . models import Room,Problem,Player
import json
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
###for get_current_users()
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core import serializers

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    logged_in_user = 0
    #print(type(user_id_list))
    #status = 'Offline'
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
        
        #user_id_list.append(('logged_in_user'))
    

    # Query all logged in users based on id list
    
    return User.objects.filter(id__in=user_id_list)

def index(request):

    #rooms = Room.objects.order_by("title")
    
    
    if request.user.is_authenticated:
        user=request.user 
        try:
                player = Player()
                player.name = user
                player.save()
        except:
            player = Player.objects.get(name=user)
                                                         
    else:
        return HttpResponseRedirect('/accounts/login/')
    


    rooms = Room.objects.filter(room_status="Open")
    print(rooms)
    return render(request, 'chat/index.html', {'rooms':rooms,})


def room(request, room_name):
    prob = Problem.objects.order_by('ques_no')
    users=list(get_current_users())

    #users.append({'logged_in_user':True})
    for user in users:
        user.status = 'Online' 
    count=0           #counting no of open rooms
    for i in Room.objects.all():
        print(i)
        if i.room_status=='Open':
            print(type(i.room_status))
            count+=1
            break         #breaks even if one room has not touched maximum players
    

    print(count)           
    print(list(Room.objects.all()))
    if count>0:
        
        if Room.objects.filter(title=room_name):
            print("this is in rooms")
            data = Room.objects.all()
            
            name = Room.objects.get(title=room_name)
            print(name)

            name.max_players += 1
            if name.max_players>20:
                name.room_status='Closed'
                name.save()
            else:
                name.save()
                
    
            
            return render(request, 'chat/room.html',
            {'room_name_json': mark_safe(json.dumps(room_name)),
            #'prob':prob,
            'users':users,
            'room_status':name.room_status
            })
            
             
        else:
            print("except")
            return HttpResponseRedirect('/chat/')
            
    else:
        print("else")
        room_name = Room()
        name=Room.objects.create(title=room_name)
        name.max_players+=1
        name.save()
        return render(request, 'chat/room.html', 
        {'room_name_json': mark_safe(json.dumps(room_name)),
        #'prob':prob,'users':users,
        'room_status':name.room_status
        })





def create_room(request):
    #room = Room.objects.create(title = room_name)

    return HttpResponseRedirect('/chat/room_name')
   
#A Feature Of Django Session----NOT used in project
"""
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

"""


        

