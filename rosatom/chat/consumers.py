import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Channel, Message
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split("token=")[-1]

        try:
            access_token = AccessToken(token)
            self.user = await database_sync_to_async(User.objects.get)(id=access_token['user_id'])
        except Exception:
            self.user = AnonymousUser()

        if self.user.is_authenticated:
            self.scope["user"] = self.user
            self.slug = self.scope['url_route']['kwargs']['slug']
            self.room_group_name = f"chat_{self.slug}"
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope["user"].username

        channel = await database_sync_to_async(Channel.objects.get)(slug=self.slug)
        await database_sync_to_async(Message.objects.create)(
            channel=channel,
            user=self.scope["user"],
            content=message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
