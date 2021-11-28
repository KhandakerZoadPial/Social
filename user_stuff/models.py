from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from datetime import datetime
from django.contrib.humanize.templatetags import humanize


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    captions = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_picture', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    number_of_love = models.IntegerField(default=0)
    is_loved = models.BooleanField(default=False)
    is_cooled = models.BooleanField(default=False)
    number_of_comment = models.IntegerField(default=0)

    def get_date(self):
        return humanize.naturaltime(self.date)

    def __str__(self):
        return str(self.user) + ' '+ str(self.date.date())

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True, default='default.jpg')
    bio = models.CharField(max_length=101, blank=True)
    gender = models.CharField(max_length=6, blank=True)
    religion = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    about_me = models.TextField(blank=True)
    favorite_quotes = models.TextField(blank=True)
    hometown = models.CharField(max_length=20, blank=True)
    current_city = models.CharField(max_length=20, blank=True)
    education = models.TextField(blank=True)
    relationship = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    number_of_friends = models.IntegerField(default=0)
    followed_by = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Love_Reaction(models.Model):
    love_user = models.ManyToManyField(User, related_name='lovingUser')
    cool_user = models.ManyToManyField(User, related_name='coolingUser')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    

    @classmethod
    def loved(cls, post, loving_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.love_user.add(loving_user)

    @classmethod
    def unloved(cls, post, unloving_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.love_user.remove(unloving_user)

    @classmethod
    def cooled(cls, post, cooling_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.cool_user.add(cooling_user)

    @classmethod
    def uncooled(cls, post, uncooling_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.cool_user.remove(uncooling_user)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_loved = models.BooleanField(default=False)
    number_of_love = models.IntegerField(default=0)


class Love_Reaction_On_Comment(models.Model):
    love_user = models.ManyToManyField(User, related_name='lovingUserofcomment')
    cool_user = models.ManyToManyField(User, related_name='coolingUserofcomment')
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)

    @classmethod
    def loved(cls, comment, loving_user):
        obj, create = cls.objects.get_or_create(comment=comment)
        obj.love_user.add(loving_user)

    @classmethod
    def unloved(cls, comment, unloving_user):
        obj, create = cls.objects.get_or_create(comment=comment)
        obj.love_user.remove(unloving_user)
    
    @classmethod
    def cooled(cls, comment, cooling_user):
        obj, create = cls.objects.get_or_create(comment=comment)
        obj.cool_user.add(cooling_user)

    @classmethod
    def uncooled(cls, comment, uncooling_user):
        obj, create = cls.objects.get_or_create(comment=comment)
        obj.cool_user.remove(uncooling_user)

    def __str__(self):
        return str(self.comment)



class BuddyList(models.Model):
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Already friend stuff
    pure_members = models.ManyToManyField(User, related_name='buddies')

    # Got request and received request stuff
    pending_users = models.ManyToManyField(User, related_name='pendingUsers')
    i_send_to = models.ManyToManyField(User, related_name='isendtoUsers')
    
    #Follow stuff
    follower_members = models.ManyToManyField(User, related_name='followers')
    i_am_following = models.ManyToManyField(User, related_name='iamfollowingusers')

    # Add stuff
    @classmethod
    def friend(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.pure_members.add(another_user)

    @classmethod
    def unfriend(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.pure_members.remove(another_user)

    # Pending stuff
    @classmethod
    def add_to_pending(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.pending_users.add(another_user)

    @classmethod
    def remove_from_pending(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.pending_users.remove(another_user)

    # send to stuff
    @classmethod
    def add_to_send_to(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.i_send_to.add(another_user)

    @classmethod
    def remove_from_send_to(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.i_send_to.remove(another_user)

    def __str__(self):
        return (f"{self.owner_user}'s buddylist")


class notification_object(models.Model):
    type_of_notification = models.IntegerField(default=0)
    # 1= love_post, 2=cool_post, 3=comment, 4=love_comment, 5=cool_comment, 6=friend_req, 7=accept_fri_req
    post_id = models.IntegerField(null=True)
    comment_id = models.IntegerField(null=True)
    done_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class NotificationList(models.Model):
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE)
    my_notis = models.ManyToManyField(notification_object, related_name='noti_obj')
    number_of_new = models.IntegerField(default=0)

    @classmethod
    def add_to_noti(cls, user, noti):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.my_notis.add(noti)

    @classmethod
    def remove_from_noti(cls, user, noti):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.my_notis.remove(noti)

    @classmethod
    def has_new(cls, user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.has_new=True

    @classmethod
    def hasnot_new(cls, user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        obj.has_new=False


class Message_List(models.Model):
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_users_list = models.ManyToManyField(User, related_name='owner_users_list')

    @classmethod
    def add(cls, user, another_user):
        obj, create = cls.objects.get_or_create(owner_user=user)
        if another_user not in cls.owner_users_list:
            obj.owner_users_list.add(another_user)


class All_messages(models.Model):
    je_dise = models.ForeignKey(User, on_delete=models.CASCADE, related_name='one')
    je_pabe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='two')
    body = models.TextField()
    
