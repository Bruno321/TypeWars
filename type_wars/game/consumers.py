import json
from asgiref.sync import async_to_sync, sync_to_async

# django
from django.contrib.auth import get_user_model

# local
from users.models import Profile

# channels
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        
        self.room_group_name = 'chat_%s' % self.room_name

        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self,close_code):
        
        # 4000 is the victory close code
        if close_code == 4000:
            if not self.scope["user"].is_anonymous:
                await database_sync_to_async(self.upload_victory_data)()
        # 4001 is the defeat close code 
        if close_code == 4001:
            if not self.scope["user"].is_anonymous :
                await database_sync_to_async(self.upload_defeat_data)()


        await self.channel_layer.group_discard(
            self.room_group_name,
            self.room_name
        )

    async def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
            }
        )


    async def chat_message(self,event):
        """
            Called when someone has messaged our chat.
        """
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message':message,
        }))

    def upload_victory_data(self):
        self.user_id = self.scope["user"].id
        User = get_user_model()
        
        self.user = User.objects.get(id=self.user_id)

        self.user.victorys = self.user.victorys + 1
        self.user.save()

    def upload_defeat_data(self):
        self.user_id = self.scope["user"].id
        User = get_user_model()
        
        self.user = User.objects.get(id=self.user_id)

        self.user.defeats = self.user.defeats + 1
        self.user.save()
        