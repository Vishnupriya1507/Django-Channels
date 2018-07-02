from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from . models import Room,Problem
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']    # here we are getting room name from url
        
        self.room_group_name = '%s' % self.room_name                    # here its making group name which i
                            
                                                                        # made it same as room name here
        

         
        """
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
        """    
        if self.room_group_name == "check_room1":
            async_to_sync(self.channel_layer.group_add)(            # SYNTAX--group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name)

        
            for i in Room.objects.all():
                if str(i)==self.room_group_name:
                    self.room_id=str(i.id)
                    print(i.id)
                    
                
            self.accept()
        elif self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_add)(            # SYNTAX--group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name)
            self.accept()
        else:                                                       # THIS BLOCK OF CODE -- is for disconnecting user 
            self.accept()                                           # who entered room name other than what are mentioned
        

        #print(self.rooms)
             

        

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
                                                            


        

        # Send message to room group
         
        if self.room_group_name =="check_room1":
            async_to_sync(self.channel_layer.group_send)(             # group_send("group_name",{"poinies":True})
               "check_room1",{'type': 'chat_message','message': message,  
                'username':self.scope["user"].username                 # Sends an event to a group.
                                                                      #An event has a special 'type' key corresponding  'message': message                                             #
                ,'room_id':self.room_id })                                  
                
                                                                      # to the name of the method that should 
                                                                     # be invoked on consumers that receive the event.
             
        if self.room_group_name =="lobby":
            async_to_sync(self.channel_layer.group_send)(
              "lobby",{'type': 'chat_message','message': message})
        print(self.scope["user"].username + "  heyyyyy")           
        
        #print(self.room_id)
        print("sd")

        #self.send(text_data=json.dumps({'message': message }))     # self.send() sends msg only to one channel 
    


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        #user = event['username']
        
        if self.room_group_name=="check_room1":
            
            self.send(text_data=json.dumps({'message': message,'username':self.scope["user"].username,'room_id':self.room_id})) 
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

            
       
            
                                  
