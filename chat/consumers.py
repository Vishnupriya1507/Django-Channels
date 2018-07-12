from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . models import Room,Problem,Player
from django.contrib.auth.models import User
from . import views
from chat.views import get_current_users
from .utils import get_room_or_error

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
        async_to_sync(self.channel_layer.group_add)(                       # group_add("group_name","channel_name")
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
        
        async_to_sync(self.channel_layer.group_discard)(      #  group_discard("group_name","channel_name")
            self.room_group_name ,self.channel_name)
        
        users=list(get_current_users())
        #users.append({'logged_in_user':True})
        print(type(get_current_users()))
        print(users)
        for user in users:
            self.user.status = 0   
        
        """
        if self.room_group_name =="check_room1":
            async_to_sync(self.channel_layer.group_discard)(      #  group_discard("group_name","channel_name")
            "vishnis" ,self.channel_name)  
                                                                 ### when only one channel then we just used pass
        elif self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_discard)(
                "lobby",self.channel_name)
        
        else:                                                  # THIS BLOCK OF CODE -- is for disconnecting user 
            self.close()                                      # who entered room name other than what are mentioned
        

        """


                                                                     
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)                 #text_data is received from frontend
        message = text_data_json['message']
        
                                                            

        

        users = list(get_current_users())
        self.user = User.objects.get(username=self.scope["user"].username)
        self.player = Player.objects.get(name = self.user)
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
        #room = get_room_or_error(self.room_id, self.scope["user"])
        
        if message=="":  #[this is for sending Question]
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(            #SYNTAX-- group_send("group_name",{"poinies":True})
               self.room_group_name,{
                'type': 'chat_message',
                'message': "", 
                'username':"From server :",                          # Sends an event to a group.
                                                                     #An event has a special 'type' key corresponding  'message': message                                             #
                'room_id':self.room_id ,                             # 'message': message         
                'room_group_name': self.room_group_name,
                'user.status':'Online',
                'ques': self.ques
                  })                                                 # to the name of the method that should 
            print("sd")                                              # be invoked on consumers that receive the event.
        
        

        else:

            async_to_sync(self.channel_layer.group_send)(            # group_send("group_name",{"poinies":True})
               self.room_group_name,{
                'type': 'chat_message',
                'message': message,  
                'username':self.scope["user"].username+"heyyyyyyyyyyyyyyyyyy",              # Sends an event to a group.
                                                                     #An event has a special 'type' key corresponding  'message': message                                             #
                'room_id':self.room_id ,                             # 'message': message         
                'room_group_name': self.room_group_name,
                'user.status':'Online',
                'ques': self.ques
                  })         

        """

        async_to_sync(self.channel_layer.group_send)(            # group_send("group_name",{"poinies":True})
           self.room_group_name,
           {'type': 'chat_message',
            'message ': "Correct Answer By :" +str(player),  
            'username':'From Server ',                           # Sends an event to a group.
                                                                 #An event has a special 'type' key corresponding  'message': message                                             #
            'room_id':self.room_id ,                             # 'message': message         
            'room_group_name': self.room_group_name,
            'user.status':'Online',
            'ques': self.ques
            })  
        async_to_sync(self.channel_layer.group_send)(            # group_send("group_name",{"poinies":True})
           self.room_group_name,
           {'type': 'chat_message',
            'message ': "NEXT QUES :" +str(player),  
            'username':'From Server ',                           # Sends an event to a group.
                                                                 #An event has a special 'type' key corresponding  'message': message                                             #
            'room_id':self.room_id ,                             # 'message': message         
            'room_group_name': self.room_group_name,
            'user.status':'Online',
            'ques': self.ques
            })  
        """



        '''                                                      
        if self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_send)(
              "lobby",{'type': 'chat.message','message':message,'username':self.scope["user"].username,'room_id':self.room_id})
        

        print(self.scope["user"].username + "  heyyyyy")
        
        #print(self.room_id)
        

        #self.send(text_data=json.dumps({'message': message }))     # self.send() sends msg only to one channel 
        '''


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user=self.scope["user"]

        message['user']="rasss"
        #user = event['username']
        if message=="":    
            self.send(text_data = json.dumps({'message': self.ques,
                'username':"FROM SERVER :",
                'room_id':event['room_id'],
                'room_group_name': event['room_group_name'],
                'user.status':'Online',
                #'ques': self.ques
                }))
        
        else:
            self.send(text_data = json.dumps({'message': message,
                'username':self.scope["user"].username,
                'room_id':event['room_id'],
                'room_group_name': event['room_group_name'],
                'user.status':'Online',
                #'ques': self.ques
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
            

                self.send(text_data = json.dumps({'message': "Correct Answer By : " + self.scope["user"].username,
                    'username':"FROM SERVER :",
                    'room_id':event['room_id'],
                    'room_group_name': event['room_group_name'],
                    'user.status':'Online',
                    #'ques': self.ques
                    })) 

            #ans = Problem.objects.get(pk=1).ques_answer
            #self.send(text_data=json.dumps({'message': "YES YOU ARE RIGHT!!!"}))
            print("sesdbgs")   
        '''
            if message==ans:

                self.send(text_data=json.dumps({'message': "YES YOU ARE RIGHT!!!"}))
            else:
                self.send(text_data=json.dumps({'message':"YOU ARE WRONG !!"})) 
            print(ans)
        # Send message to WebSocket
        # self.send(text_data=json.dumps({'message': message})) 
        '''
    
          
       
            
                                  