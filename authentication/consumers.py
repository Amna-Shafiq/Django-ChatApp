
from django.utils import timezone
import json
import base64
from django.core.files.base import ContentFile
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        print("Connected")

    def receive(self, text_data):  # responsible for receiving messages from the WebSocket connection
        from .models import User
        message = json.loads(text_data)
        message_type = message.get('type')
        if message_type == 'chat':
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            chat_room_id = text_data_json['chat_room_id']
            username = text_data_json['username']
            user = User.objects.get(username=username)
            user_id = user.id
            print("receive web socket msg")
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'chat_room_id': chat_room_id,
                    'username': username,
                    'user_id': user_id
                }
            )
        elif message_type == 'image':
            chat_room_id = message.get('chat_room_id')
            image_data = message.get('image')
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'image_message',
                    'image_data': image_data,
                    'username': self.scope['user'].username,
                    'chat_room_id': chat_room_id,
                }
            )
        elif message_type == 'audio':
            chat_room_id = message.get('chat_room_id')
            audio_data = message.get('audioURL')
            try:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'audio_message',
                        'audio_data': audio_data,
                        'username': self.scope['user'].username,
                        'chat_room_id': chat_room_id,
                    }
                )
            except Exception as e:
                print(f"Exception occurred in audio_message: {e}")

    def chat_message(self, event):
        from .models import Message, ChatRoom, User
        message = event['message']
        username = event['username']
        chat_room = ChatRoom.objects.get(id=event['chat_room_id'])
        user_id = event['user_id']
        user = User.objects.get(id=user_id)

        if username == self.scope["user"].username:
            new_message = Message(user=user, content=message,
                                  date_added=timezone.now(), chat_room=chat_room)
            new_message.save()

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'username': user.username,
            'timestamp': timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')
        }))

    def image_message(self, event):
        from .models import Message, ChatRoom, User
        image_data = event['image_data']
        username = event['username']
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        chat_room = ChatRoom.objects.get(id=event['chat_room_id'])

        user = User.objects.get(username=username)
        username = user.username

        if username == self.scope["user"].username:
            new_message = Message(
                user=user, image=image_data, date_added=timezone.now(), chat_room=chat_room)
            new_message.save()
        self.send(text_data=json.dumps({
            'type': 'image',
            'username': username,
            'timestamp': timestamp,
            'image': image_data,
        }))

    def audio_message(self, event):
        from .models import Message, ChatRoom, User
        username = event['username']
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        chat_room = ChatRoom.objects.get(id=event['chat_room_id'])
        user = User.objects.get(username=username)
        username = user.username
        if username == self.scope["user"].username:
            new_message = Message(
                user=user,
                audio=event['audio_data'],
                date_added=timezone.now(),
                chat_room=chat_room,
            )
            new_message.save()
        self.send(text_data=json.dumps({
            'type': 'audio',
            'username': username,
            'timestamp': timestamp,
            'audioURL': event['audio_data'],
        }))
