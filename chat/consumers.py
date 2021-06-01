import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        await self.accept()

        self.room_group_id = self.scope['url_route']['kwargs']['room_id']
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

    async def disconnect(self, _close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.createMessage(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_id,
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
        room = Room.objects.get(
            id=self.room_group_id
        )
        Message.objects.create(
            room=room,
            content=event['message'],
            posted_by=self.scope['user'],
        )
