from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']    #here we are getting room name
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(            # group_add("group_name","channel_name")
            self.room_group_name,
            self.channel_name
        )
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.accept()
        self.rooms = set()
        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(           #  group_discard("group_name","channel_name")
            self.room_group_name,
            self.channel_name
        )                                                         ### when only one channel then we just used pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(              # group_send("group_name",{"poinies":True})
            self.room_group_name,
            {                                                  # Sends an event to a group.
                'type': 'chat_message',                       #An event has a special 'type' key corresponding                'message': message                             #
                 
                 'message': message
            }                                                  # to the name of the method that should 
                                                               #be invoked on consumers that receive the event.
        )
    
        print("sd")

        #self.send(text_data=json.dumps({'message': message }))     # self.send() sends msg only to one channel 
    


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))       
                                    