from django.db import models
from .user import User
from django.core.exceptions import ValidationError

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name='chat_rooms1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_rooms2', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user1', 'user2')
    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError('User1 and User2 cannot be the same.')
    def save(self, *args, **kwargs):
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1

        self.clean() 
        super().save(*args, **kwargs)
# In the save method, the code is checking if the id of user1 is greater than the id of user2. If it is, then 
# it means that user2 was created before user1. In that case, the code swaps user1 and user2 so that user1 
# is always the user with the lower id.
# The purpose of this is to ensure that there is consistency in the way 
# the ChatRoom objects are created. This ensures that the same ChatRoom object 
# is created regardless of whether user1 or user2 is created first.