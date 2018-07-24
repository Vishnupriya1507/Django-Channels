from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . models import Room,Problem,Player
from django.contrib.auth.models import User
from . import views
from chat.views import get_current_users
from django.core import serializers


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']    # here we are getting room name from url
        
        self.room_group_name = '%s' % self.room_name                       # here its making group name which i
                                                                           # made it same as room name here
        
        for i in Room.objects.all():
            if str(i)==self.room_group_name:
                self.room_id=i.id
                break
        async_to_sync(self.channel_layer.group_add)(                       # group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name
        )
        self.accept()

                                     
            
                                                                        #print("helloooooooo") 
                                                                        #queryset = get_current_users()
                                                                        #print(list(queryset))
                                                                        #print(queryset.exists())
                                                                        #print(queryset.count())    
           
            
        
        # Join room group
        '''
        async_to_sync(self.channel_layer.group_add)(                     # group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name
        )

        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.accept()
        
        '''
         # Reject the connection
        #self.close()
        
            # Accept the connection
            

        

    def disconnect(self):
        # Leave room group
        
        

        self.player = request.user
        print("yoyoyoyo")
        print(player)
        Player.objects.get(name=player).delete()
        users=list(get_current_users())
        #users.append({'logged_in_user':True})
        print(type(get_current_users()))
        print(users)
        for user in users:
            self.user.status = 0   
        
        async_to_sync(self.channel_layer.group_discard)(      #SYNTAX----group_discard("group_name","channel_name")
            self.room_group_name ,self.channel_name)
        
        """
        SYNTAX--

        if self.room_group_name =="check_room1":
            async_to_sync(self.channel_layer.group_discard)(     #  group_discard("group_name","channel_name")
            self.room_group_name ,self.channel_name)  
                                                                 ### when only one channel then we just used pass
        elif self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,self.channel_name)
        
        else:                                                  # THIS BLOCK OF CODE -- is for disconnecting user 
            self.close()                                      # who entered room name other than what are mentioned
        

        """


                                                                     
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)                 #text_data is received from frontend
        message = text_data_json['message']
        msg_typed = text_data_json['msg_typed']
        user_ = text_data_json['user_']
        
        #print(msg_typed) ----   {"message":"","user_":"rashi","msg_typed":true}
        
        print(text_data_json)

        users = list(get_current_users())
        for user in users:
            user.status = 'Online' 
        
        
        self.user = User.objects.get(username=self.scope["user"].username)
        print(self.user)

        self.player = Player.objects.get(name = self.user)  #--------- player logging in
        
        print(self.player)
        
        
        

        


        
        self.dict_ = {}                #-------------{player_name : player_score}
        
        players = Player.objects.all()

        print("heyyyyheyyyyheyyyyheyyyyheyyyyheyyyy")
        print(type(players))
        


        data = []
        print(players)
        for player_ob in players:
            
            if player_ob.room ==self.room_name:
                
                print(type(player_ob.name))
                d = []
                d.append(player_ob.name.username)
                d.append(player_ob.score)
                print(d)
                data.append(d)
                self.dict_["room_name"] = self.room_name
                self.dict_["data"]=data
                        
                
        
        print(data)                #-----[['abc', 2100], ['f20170325', 1100]]

        print(self.dict_)          #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
           
        




        
        
        
        print(type(self.user))
        self.room = Room.objects.get(title =self.room_group_name)
        print("receive")
        print(type(self.room))
        self.player.ans_given = message
        self.player.room = self.room.title
        self.player.save()
        
        self.ans= Problem.objects.get(pk= self.room.ques_num ).ques_answer 
        print(self.ans)
        self.ques_No = Problem.objects.get(pk = self.room.ques_num)
        self.ques = self.ques_No.prob_ques
        
        print(type(self.ques))
        
        print(self.user)
        
        
        if message=="":      #----------[this is for sending Question]
            

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(            #SYNTAX-- group_send("group_name",{"poinies":True})
               self.room_group_name,{
                'type': 'chat_message',
                'message': "", 
                'username':"From server :",                          # Sends an event to a group.
                                                                     # An event has a special 'type' key corresponding  'message': message                                             #
                'room_id':self.room_id ,                             # 'message': message         
                                                                     # to the name of the method that should  be invoked on consumers that receive the event.
                'room_group_name': self.room_group_name,  #---------room-name
                
                'user.status':'Online',
                
                'ques': self.ques,
                
                'msg_typed':False,
                
                'dict_':self.dict_    #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                })                                                    
            print("sd")                                              
        
        

        else:
            msg_typed = True
            async_to_sync(self.channel_layer.group_send)(            # group_send("group_name",{"poinies":True})
               self.room_group_name,{
                'type': 'chat_message',
                'message': message,  
                'username':user_,                                    # Sends an event to a group.
                                                                     #An event has a special 'type' key corresponding  'message': message                                             #
                'room_id':self.room_id ,                             # 'message': message         
                
                'room_group_name': self.room_group_name,
                
                'user.status':'Online',
                
                'msg_typed':True,
                
                'dict_':self.dict_    #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                  })         

        


    

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        msg_typed=event['msg_typed']
        user_= event['username']
        
        dict_=event['dict_']    #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
        
        # {'message': 'football', 'msg_typed': True, 'other_user': 'rashi', 'user_': 'trs'}
        print(event)


        if message=="":    
            self.send(text_data = json.dumps({'message': self.ques,
                'username':"FROM SERVER :",
                'room_id':event['room_id'],
                'room_group_name': event['room_group_name'],
                'user.status':'Online',
                'msg_typed':False,
                

                'dict_':dict_     #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                }))
        
        else:
            msg_typed = True
            self.send(text_data = json.dumps({'message': message,
                'username':user_,
                'room_id':event['room_id'],
                'room_group_name': event['room_group_name'],
                'user.status':'Online',
                'msg_typed':True,
                
                'dict_':dict_      #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                }))

            self.player.ans_given = message
            self.player.save()

            if self.player.ans_given == self.ans:
                self.room.ques_num += 1
                self.player.score += 100
                self.ques_No = Problem.objects.get(pk = self.room.ques_num)
                self.ques = self.ques_No.prob_ques
                self.ans= Problem.objects.get(pk= self.room.ques_num ).ques_answer 
                self.player.save()
                self.room.save()


                self.send(text_data = json.dumps({'message': "Correct Answer By : " + user_,
                    'username':"FROM SERVER :",
                    'room_id':event['room_id'],
                    'room_group_name': event['room_group_name'],
                    'user.status':'Online',
                    'msg_typed':False,
                    
                    'dict_':dict_   #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                })) 
            

                message = ""
                self.send(text_data = json.dumps({'message': self.ques,
                'username':"FROM SERVER :",
                'room_id':event['room_id'],
                'room_group_name': event['room_group_name'],
                'user.status':'Online',
                'msg_typed':False,
                
                'dict_':dict_       #-----{"room_name": "room1", "data": [["abc", 2100], ["f20170325", 1100]]}
                }))
        print("sesdbgs")   
        

        #SYNTAX--
        # Send message to WebSocket
        # self.send(text_data=json.dumps({'message': message})) 
        
    
          
       
            
                                  