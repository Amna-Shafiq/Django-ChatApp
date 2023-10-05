from rest_framework import serializers
from .models import ChatRoom, Message,User

class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()
    last_message_timestamp = serializers.SerializerMethodField()
    other_user_id = serializers.SerializerMethodField()
    other_user_profile_image = serializers.SerializerMethodField()

    def get_last_message(self, chat_room):
        last_message = chat_room.messages.last()
        if last_message:
            return last_message.content
        return None
    
    def get_other_user(self, chat_room):
        request = self.context.get('request')
        if request and request.user:
            if chat_room.user1 == request.user:         
                return chat_room.user2.username
            else:              
                return chat_room.user1.username
        return None
    
    def get_other_user_id(self, chat_room):
        request = self.context.get('request')
        if request and request.user:
            if chat_room.user1 == request.user:
                return chat_room.user2.id
            else:
                return chat_room.user1.id
        return None

    def get_last_message_timestamp(self, chat_room):
        last_message = chat_room.messages.last()
        if last_message:
            return last_message.date_added
        return None
    
    def get_other_user_profile_image(self, chat_room):
        other_user = self.get_other_user(chat_room)
        if other_user:
            other_user_instance = User.objects.get(username=other_user)
            if other_user_instance.profile_image:
                return other_user_instance.profile_image.url
        return None
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'last_message','other_user','last_message_timestamp','other_user_id','other_user_profile_image']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user', 'content', 'date_added']
