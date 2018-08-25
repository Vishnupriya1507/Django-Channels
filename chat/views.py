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


#@login_required
def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    logged_in_user = 0
    
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
        
        

    # Query all logged in users based on id list
    
    return User.objects.filter(id__in=user_id_list)

def logout(request):
    logout(request)
    return HttpResponseRedirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://127.0.0.1:8000')

#@login_required
def index(request):

    
    
    if request.user.is_authenticated:
        user = request.user 
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
    


#@login_required
def room(request, room_name):
    prob = Problem.objects.order_by('ques_no')
    users = list(get_current_users())

    print(request.user)
    player_joined = request.user  #--------- player logging in
    
    player = Player.objects.get(name=player_joined)
    player.room = room_name
    player.save()
    
    
    dict_ = {}                #-------------{player_name : player_score}
        
    players = Player.objects.all()
    
    for player in players:
        
        if player.room ==room_name:
            
            print(player.name)
    
            dict_[player]= player.score
            #self.dict_[player_ob]=str(self.dict_[player_ob]) 
            #print(type(self.dict_[player_ob]))
    
            
    
    print(dict_)                #-----{<Player: abc>: 1800, <Player: trs>: 10000, <Player: f20170325>: 1100}

    


    for user in users:
        user.status = 'Online' 
    
    
           

         

    count=0                     #-------counting no of open rooms
    for i in Room.objects.all():
        #print(i)
        if i.room_status=='Open':
            print(type(i.room_status))
            count+=1
            break               #--------breaks even if one room has not touched max players
    

    print(count)           
    print(list(Room.objects.all()))
    

    if count>0:
        
        if Room.objects.filter(title=room_name):
            print("this is in rooms")
            data = Room.objects.all()
            print(type(request.user.username))
            user = Player.objects.get(name=request.user)
            print(user)

            name = Room.objects.get(title=room_name)
            print(name)
            
                
            if user.room!=room_name:
                #print(playa)

                name.max_players += 1
                if name.max_players>20:
                    name.room_status='Closed'
                    name.save()
                else:
                    name.save()

                
    
            
            return render(request, 'chat/room.html',
            {'room_name_json': mark_safe(json.dumps(room_name)),
            #'user':request.user.username,
            
            #'users':users,
            'room_status':name.room_status
            })
            
             
        else:
            print("except")
            return HttpResponseRedirect('/chat/')
            
    else:                     #------------- else part is count = 0 here means no rooms having room_status = "Open"
        print("else")
        create_room()
        
     

@login_required
def create_room(request):     # called only when all rooms have reached their max no of players i.e 20
    room_name = Room()

    count = 0                 # counts number of rooms which are closed and then makes new room accordingily 
    for room in Room.objects.all():
        count +=1
    count +=1
    name = Room.objects.create(title = "Room"+str(count))
    name.max_players+=1
    name.room_status="Open"
    name.save()
    name = "Room"+str(count+1)
    url = '/chat/'+ name+'/'
    return HttpResponseRedirect(url)

def login(request):
    return render(request,'registration/login.html/')

    


# A Feature Of Django Session----NOT used in project

"""

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

"""




        

