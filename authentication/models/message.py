from django.db import models
from .user import User
# from .chatroom import ChatRoom
# from authentication.models.chatrooms import ChatRoom
from .chatroom import ChatRoom

class Message(models.Model):
    user = models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)
    content = models.TextField(blank=True)  # Text content (optional)
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)  # Image field
    date_added = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE, default=None)
    audio = models.FileField(upload_to='audio_messages/', blank=True, null=True)
    class Meta:
        ordering = ('date_added',)
        
  #Meta class is an inner class in Django models.
  # Which contain Meta options(metadata) that are used to change the behavior of your model fields 
  # like changing order options
