from django.forms import ModelForm
from .models import User, Advertisement, Message
from django.contrib.auth.forms import UserCreationForm  # for user create form

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1','password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name','last_name','username', 'email']
        
class AdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at','category']  
      
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']