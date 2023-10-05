from django import forms
from authentication.models import User

class ImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'