import json
from asgiref.sync import async_to_sync, sync_to_async

# django


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

        # user = self.scope['user']
        # if user.is_anonymous :
        #     user = 'Guest'
        # else:
        #     user = user.username
        
        await self.accept()

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type':'chat_message',
        #         'message': {
        #             'message': user
                    
        #         }
        #     }
        # )

        # esto es un echo, solo el que lo ocasiona lo puede ver
        # await self.send(text_data=json.dumps({
        #     'usuario': user
        # }))
        # podemos usar await self.close() si se mete mas de uno

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.room_name
        )

    async def receive(self,text_data):
        print("recibido texto",text_data)
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
            # 'user':self.scope['user'].username
        }))