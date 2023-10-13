from django.contrib import admin

# Register your models here.
from .models import User, Category, Advertisement, Message, MessageType

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(Message)
admin.site.register(MessageType)