import asyncio
import json

from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Room, Message


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)

        self.invite = self.scope['url_route']['kwargs']['invite']
        self.user = self.scope['user']

        self.room = await self.fetch_room(self.invite)
        self.roomid = f'room_{self.invite}'
        await self.channel_layer.group_add(self.roomid, self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print('received', event)
        if 'text' in event:
            data = json.loads(event['text'])
            response = json.dumps({
                'username': self.user.username,
                'content': data['content']
            })

            # broadcasts message to each websocket client
            await self.channel_layer.group_send(self.roomid, {"type": "chat_message", "text": response})
            await self.create_message(data['content'])

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('message?', event)
        # Sends message to each browser (client)
        await self.send({'type': 'websocket.send', 'text': event['text']})

    @database_sync_to_async
    def fetch_room(self, invite):
        return Room.objects.get(invite=invite)

    @database_sync_to_async
    def create_message(self, content):
        return Message.objects.create(content=content, room=self.room, author=self.user)

