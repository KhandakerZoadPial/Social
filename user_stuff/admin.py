from django.contrib import admin
from .models import Post, User_Profile, Love_Reaction, Comment, Love_Reaction_On_Comment, BuddyList, notification_object, NotificationList, Message_List


# Register your models here.
admin.site.register(Post)
admin.site.register(User_Profile)
admin.site.register(Love_Reaction)
admin.site.register(Comment)
admin.site.register(Love_Reaction_On_Comment)
admin.site.register(BuddyList)
admin.site.register(notification_object)
admin.site.register(NotificationList)
admin.site.register(Message_List)
