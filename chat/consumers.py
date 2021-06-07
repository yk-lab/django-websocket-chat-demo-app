from logging import getLogger

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models.member import Member

from .models import Message, Room

logger = getLogger(__name__)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    groups = ['broadcast']

    async def connect(self):
        try:
            self.room = await self.get_object()
            await self.accept()
        except Room.DoesNotExist:
            logger.info(f'Room DoesNotExist: {self.scope}')
            await self.close()
        else:
            await self.channel_layer.group_add(
                str(self.room.id),
                self.channel_name,
            )
            await self.add_member()
            await self.channel_layer.group_send(
                str(self.room.id),
                {
                    'type': 'join',
                    'user': self.scope['user'].get_username(),
                }
            )

    async def disconnect(self, _close_code):
        await self.channel_layer.group_send(
            str(self.room.id),
            {
                'type': 'leave',
                'user': self.scope['user'].get_username(),
            }
        )
        await self.channel_layer.group_discard(
            str(self.room.id),
            self.channel_name,
        )
        await self.disconnect_member()
        await self.close()

    async def receive_json(self, data):
        type = data['type']
        if type == 'heartbeat':
            await database_sync_to_async(
                Member.objects.touch)(self.channel_name, room_id=self.room.id)
            return

        message = data['message']
        await self.create_message(data)
        await self.channel_layer.group_send(
            str(self.room.id),
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].get_username(),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        await self.send_json({
            'type': 'chat_message',
            'message': message,
            'user': user,
        })

    async def join(self, event):
        await self.send_json(event)

    async def leave(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def get_object(self):
        room_id = self.scope['url_route']['kwargs']['room_id']
        return Room.objects.get(pk=room_id)

    @database_sync_to_async
    def add_member(self):
        self.member = self.room.add_member(
            self.channel_name, self.scope['user'], True)

    @database_sync_to_async
    def disconnect_member(self):
        self.member.is_online = False
        self.member.save()

    @database_sync_to_async
    def create_message(self, event):
        Message.objects.create(
            room_id=self.room.id,
            content=event['message'],
            posted_by=self.scope['user'],
        )
