import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        await self.accept()

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name,
        )

    async def disconnect(self, _close_code):
        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name,
        )
        await self.close()

    async def receive_json(self, data):
        message = data['message']
        await self.createMessage(data)
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].email,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def createMessage(self, event):
        Message.objects.create(
            room_id=self.room_id,
            content=event['message'],
            posted_by=self.scope['user'],
        )
