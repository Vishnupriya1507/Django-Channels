from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . models import Room,Problem
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']    # here we are getting room name from url
        self.room_group_name = '%s' % self.room_name                       # here its making group name which i 
        print (self.room_group_name)                                       # made it same as room name here
        users = list(User.objects.all()) 
        print('all users in chat consumer:', users)
         

        # Join room group
        '''
        async_to_sync(self.channel_layer.group_add)(                       # group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name
        )

        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.accept()
        #self.rooms = set()
        '''
        #self.user = scope["user"]
        if self.scope["user"].is_anonymous:
            print(self.scope["user"].username + "  heyyyyy")
            # Reject the connection
            self.close()
        else:
            # Accept the connection
            
            if self.room_group_name == "check_room1":
                async_to_sync(self.channel_layer.group_add)(            # SYNTAX--group_add("group_name","channel_name")
                self.room_group_name,
                self.channel_name)
                print (self.channel_name + "hoiiiiii")
                self.accept()
            elif self.room_group_name =="lobby":
                async_to_sync(self.channel_layer.group_add)(            # SYNTAX--group_add("group_name","channel_name")
                self.room_group_name,
                self.channel_name)
                self.accept()
            else:                                                       # THIS BLOCK OF CODE -- is for disconnecting user 
                self.accept()                                           # who entered room name other than what are mentioned

              

        

    def disconnect(self):
        # Leave room group
        if self.room_group_name =="check_room1":
            async_to_sync(self.channel_layer.group_discard)(      #  group_discard("group_name","channel_name")
            "vishnis" ,self.channel_name)  
                                                                 ### when only one channel then we just used pass
        elif self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_discard)(
                "lobby",self.channel_name)
        
        else:                                                  # THIS BLOCK OF CODE -- is for disconnecting user 
            self.close()                                      # who entered room name other than what are mentioned

                                                                     
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)             # text_data is received from frontend
        message = text_data_json['message']
                                                            #user = text_data_json['username']
        #self.user = scope["user"]
        
        # Send message to room group
         
        if self.room_group_name =="check_room1":
            async_to_sync(self.channel_layer.group_send)(             # group_send("group_name",{"poinies":True})
               "check_room1",{'type': 'chat_message','message': message})   ##,'username':user
                                                                      # Sends an event to a group.
                                                                      #An event has a special 'type' key corresponding                                          #
                                                                      # 'message': message   
                 
                                                                      # to the name of the method that should 
                                                                     # be invoked on consumers that receive the event.
             
        elif self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_send)(
              "lobby",{'type': 'chat_message','message': message})
        
        print("sd")

        #self.send(text_data=json.dumps({'message': message }))     # self.send() sends msg only to one channel 
    


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        #user = event['username']
        print("ddd")
        if self.room_group_name=="check_room1":
            
            self.send(text_data=json.dumps({'message': message})) 
            ques = Problem.objects.get(pk=1).prob_ques
            self.send(text_data=json.dumps({'message': ques})) 
            ans = Problem.objects.get(pk=1).answer
            if message==ans:
                self.send(text_data=json.dumps({'message': "YES YOU ARE RIGHT!!!"}))
            else:
                self.send(text_data=json.dumps({'message':"YOU ARE WRONG !!"})) 
            print(ans)
        # Send message to WebSocket
        # self.send(text_data=json.dumps({'message': message})) 

            
             
            
                                  