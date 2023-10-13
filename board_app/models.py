from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.files.base import ContentFile


class User(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    confirmation_code = models.CharField(max_length=6, default = '')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class Category(models.Model):
    name = models.CharField(max_length=128) 
    description = models.TextField(null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Advertisement(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.ImageField(null=True, blank = True)
    img_thumb = models.ImageField(null=True, blank = True)
    video = models.FileField(null=True, blank = True)
    
    def save(self):
        self.img_thumb = ContentFile(self.img.read())
        new_picture_name = self.img.name.split("/")[-1]
        self.img_thumb.name = new_picture_name
        super().save()  # saving image first
        if self.img.url:
            img_temp = Image.open(self.img.path) # Open image using self
            img_size = 200
            if img_temp.height > img_size or img_temp.width > img_size:
                new_img = (img_size, img_size)
                img_temp = img_temp.resize(new_img)
                img_temp.save(self.img_thumb.path)  # saving image at the same path
                
    
    def __str__(self):
        return self.title

class MessageType(models.Model):
    name = models.CharField(max_length=250) 
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='user_sender')
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_receiver')
    type = models.ForeignKey(MessageType, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    text = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text
