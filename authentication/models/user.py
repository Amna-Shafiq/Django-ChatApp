# from django.db import models
# from django.contrib.auth.models import User 
# from pathlib import Path
# from django.core.exceptions import ValidationError
# # from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError


from django.db import models
from django.contrib.auth.models import User 

class User(User):
    profile_image = models.ImageField(default="flower.webp",upload_to='uploads/')
    # def clean(self):
    #     super().clean()
    #     # Validate first name
    #     if not self.first_name:
    #         raise ValidationError("First name is required.")
    #     # Validate last name
    #     if not self.last_name:
    #         raise ValidationError("Last name is required.")
        
    # def save(self, *args, **kwargs):
    #     self.clean() 
    #     super().save(*args, **kwargs)
   
    def __str__(self):
        return self.username
