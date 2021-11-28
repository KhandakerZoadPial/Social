from django.shortcuts import render, redirect, HttpResponse
from .models import Post, User_Profile, Love_Reaction, Comment, Love_Reaction_On_Comment, BuddyList, notification_object, NotificationList, Message_List, All_messages
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.db.models import Q
from django.core.paginator import Paginator


@login_required(login_url='login')
def user_home(request):
    user = request.user
    try:
        my_buddy_list = BuddyList.objects.get(owner_user=user)
        my_buddy_list = my_buddy_list.pure_members.all()
        my_buddy_list = list(my_buddy_list)
        my_buddy_list.append(user)
        all_post = Post.objects.filter(user__in=my_buddy_list).order_by('-date')   
        
    except:
        all_post = Post.objects.filter(user=user).order_by('-date')
        
    for post in all_post:
        if Love_Reaction.objects.filter(post=post, love_user=user):
            post.is_loved = True
        elif Love_Reaction.objects.filter(post=post, cool_user=user):
            post.is_cooled = True
    p=Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    data = {
        'posts': page_obj
    }
    return render(request, 'user_stuff/news_feed.html', data)


@login_required(login_url='login')
def post(request):
    if request.method == 'POST':
        imagex = request.FILES.get('image')
        captionx = request.POST.get('caption', '')
        userx = request.user


        if imagex is None and captionx=='':
            messages.error(request, 'Nothing to Post..!')
            return redirect('/home')

        post_object = Post(user=userx, captions=captionx, image=imagex)
        post_object.save()
        messages.success(request, 'Your post is published.')
        return redirect('/home')
    else:
        return user_home(request)



@login_required(login_url='login')
def delete_post(request, post_id):
    try:
        post_object = Post.objects.get(pk=post_id)
    except:
        messages.error(request, 'Something went wrong.')
        return redirect('/home')

    if post_object.user==request.user:
        x = notification_object.objects.filter(post_id=post_id)
        for i in x:
            i.delete()
        post_object.delete()
        messages.info(request, 'Post deleted successfully.')
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    else:
        messages.error(request, 'Something went wrong.')
        return redirect('/home')



@login_required(login_url='login')
def user_profile(request, username):
    if request.method == 'GET':
        try:
            user_ = User.objects.get(username=username)
            usr_profile = User_Profile.objects.get(user=user_)
            usr_posts = Post.objects.filter(user=user_).order_by('-date')
            usr= request.user
            for p in usr_posts:
                if Love_Reaction.objects.filter(post=p, love_user=usr):
                    p.is_loved= True
                elif Love_Reaction.objects.filter(post=p, cool_user=usr):
                    p.is_cooled=True
            temp=''
            if BuddyList.objects.filter(owner_user=usr, pure_members=user_):
                temp = 'friend'
            elif BuddyList.objects.filter(owner_user=usr, pending_users=user_):
                temp= 'pending'
            elif BuddyList.objects.filter(owner_user=usr, i_send_to=user_):
                temp = 'sent'
            
        except:
            messages.error(request, 'No such user found')
            return redirect('/home')

        return render(request, 'user_stuff/user_profile.html', {'usr': usr_profile, 'posts': usr_posts, 'typ':temp})
        
    else:
        return redirect('/home')


@login_required(login_url='login')
def love_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        messages.error(request, 'Post does not even exist!')
        return redirect('/home')
    post = Post.objects.get(pk=post_id)
    user = request.user
    is_loved = Love_Reaction.objects.filter(post=post, love_user=user)
    is_cooled = Love_Reaction.objects.filter(post=post, cool_user=user)

    if is_cooled:
        Love_Reaction.uncooled(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love-=1
        x.save()
        if user!=post.user:
            t = notification_object.objects.get(type_of_notification=2, post_id=post_id, done_by=user)
            NotificationList.remove_from_noti(post.user, t)
            t.delete()
    if is_loved:
        Love_Reaction.unloved(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love-=1
        x.save()
        if user!=post.user:
            t = notification_object.objects.get(type_of_notification=1,post_id=post_id, done_by=user)
            NotificationList.remove_from_noti(post.user, t)
            t.delete()
    else:
        Love_Reaction.loved(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love+=1
        x.save()
        if user!=post.user:
            t = notification_object(type_of_notification=1, post_id=post_id, done_by=user)
            t.save()
            NotificationList.add_to_noti(post.user, t)
            t= NotificationList.objects.get(owner_user=post.user)
            t.number_of_new+=1
            t.save()
    try:
        addr = request.META['HTTP_REFERER']
        return redirect(addr+'#'+str(post_id))
    except:
        return redirect('/home')


@login_required(login_url='login')
def love_post2(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        messages.error(request, 'Post does not even exist!')
        return redirect('/home')
    user = request.user
    is_loved = Love_Reaction.objects.filter(post=post, love_user=user)
    is_cooled = Love_Reaction.objects.filter(post=post, cool_user=user)

    if is_loved:
        Love_Reaction.unloved(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love-=1
        x.save()
        if user!=post.user:
            t = notification_object.objects.get(type_of_notification=1,post_id=post_id, done_by=user)
            NotificationList.remove_from_noti(post.user, t)
            t.delete()
    if is_cooled:
        Love_Reaction.uncooled(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love-=1
        x.save()
        if user!=post.user:
            t = notification_object.objects.get(type_of_notification=2,post_id=post_id, done_by=user)
            NotificationList.remove_from_noti(post.user, t)
            t.delete()
    else:
        Love_Reaction.cooled(post, user)
        x = Post.objects.get(pk=post_id)
        x.number_of_love+=1
        x.save()
        if user!=post.user:
            t = notification_object(type_of_notification=2, post_id=post_id, done_by=user)
            t.save()
            NotificationList.add_to_noti(post.user, t)
            t= NotificationList.objects.get(owner_user=post.user)
            t.number_of_new+=1
            t.save()
    try:
        addr = request.META['HTTP_REFERER']
        return redirect(addr+'#'+str(post_id))
    except:
        return redirect('/home')


@login_required(login_url='login')
def comment_on_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except:
        messages.error(request, 'Post does not even exist!')
        return redirect('/home')
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text!='' and  comment_text.isspace()==False:
            x = Comment(post=post, user=request.user, comment_text=comment_text)
            x.save()
            post.number_of_comment+=1
            post.save()
            if post.user!=request.user:
                t = notification_object(type_of_notification=3, post_id=post.id, comment_id=x.id, done_by=request.user)
                t.save()
                NotificationList.add_to_noti(post.user, t)
                t= NotificationList.objects.get(owner_user=post.user)
                t.number_of_new+=1
                t.save()
            try:
                addr = request.META['HTTP_REFERER']
                return redirect(addr+'#'+str(x.id))
            except:
                return redirect('/home')
        else:
            messages.error(request, 'Something went wrong.')
            try:
                addr = request.META['HTTP_REFERER']
                return redirect(addr)
            except:
                return redirect('/home')
    elif request.method == 'GET':
        all_comment = Comment.objects.filter(post=post).order_by('-date')
        usr = request.user
        for c in all_comment:
            if Love_Reaction_On_Comment.objects.filter(comment=c, love_user=usr):
                c.is_loved= True
            elif Love_Reaction_On_Comment.objects.filter(comment=c, cool_user=usr):
                c.is_cooled=True
        if Love_Reaction.objects.filter(post=post, love_user=usr):
            post.is_loved=True
        elif Love_Reaction.objects.filter(post=post, cool_user=usr):
            post.is_cooled=True
        return render(request, 'user_stuff/comment_or_post_detail.html', {'post': post, 'comments': all_comment})


@login_required(login_url='login')
def delete_comment(request, comment_id):
    try:
        comment_object = Comment.objects.get(pk=comment_id)
    except:
        messages.error(request, 'Something went wrong.')
        return redirect('/home')

    if comment_object.user == request.user:
        x= comment_object.post
        x.number_of_comment-=1
        x.save()
        
        t =  notification_object.objects.filter(comment_id=comment_id)
        for i in t:
            i.delete()
        comment_object.delete()
        messages.success(request, 'Comment deleted.')
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    else:
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    

@login_required(login_url='login')
def love_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    user = request.user

    is_loved = Love_Reaction_On_Comment.objects.filter(comment=comment, love_user=user)
    is_cooled = Love_Reaction_On_Comment.objects.filter(comment=comment, cool_user=user)

    if is_cooled:
        Love_Reaction_On_Comment.uncooled(comment, user)
        comment.number_of_love-=1
        comment.save()
        if user!=comment.user:
            t = notification_object.objects.get(type_of_notification=5, comment_id=comment.id, done_by=user)
            NotificationList.remove_from_noti(comment.user, t)
            t.delete()
    if is_loved:
        Love_Reaction_On_Comment.unloved(comment, user)
        comment.number_of_love-=1
        comment.save()
        if user!=comment.user:
            t = notification_object.objects.get(type_of_notification=4,comment_id=comment.id, done_by=user)
            NotificationList.remove_from_noti(comment.user, t)
            t.delete()
    else:
        Love_Reaction_On_Comment.loved(comment, user)
        comment.number_of_love+=1
        comment.save()
        if user!=comment.user:
            t= notification_object(type_of_notification=4, comment_id=comment.id,post_id=comment.post.id,  done_by=user)
            t.save()
            NotificationList.add_to_noti(comment.user, t)
            t= NotificationList.objects.get(owner_user=comment.user)
            t.number_of_new+=1
            t.save()
    try:
        addr = request.META['HTTP_REFERER']
        return redirect(addr+'#'+str(comment_id))
    except:
        return redirect('/home')


@login_required(login_url='login')
def love_comment2(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    user = request.user

    is_loved = Love_Reaction_On_Comment.objects.filter(comment=comment, love_user=user)
    is_cooled = Love_Reaction_On_Comment.objects.filter(comment=comment, cool_user=user)

    if is_loved:
        Love_Reaction_On_Comment.unloved(comment, user)
        comment.number_of_love-=1
        comment.save()
        if user!=comment.user:
            t = notification_object.objects.get(type_of_notification=4, comment_id=comment.id, done_by=user)
            NotificationList.remove_from_noti(comment.user, t)
            t.delete()
    if is_cooled:
        Love_Reaction_On_Comment.uncooled(comment, user)
        comment.number_of_love-=1
        comment.save()
        if user!=comment.user:
            t = notification_object.objects.get(type_of_notification=5, comment_id=comment.id, done_by=user)
            NotificationList.remove_from_noti(comment.user, t)
            t.delete()
    else:
        Love_Reaction_On_Comment.cooled(comment, user)
        comment.number_of_love+=1
        comment.save()
        if user!=comment.user:
            t= notification_object(type_of_notification=5, comment_id=comment.id,post_id=comment.post.id,  done_by=user)
            t.save()
            NotificationList.add_to_noti(comment.user, t)
            t= NotificationList.objects.get(owner_user=comment.user)
            t.number_of_new+=1
            t.save()
    try:
        addr = request.META['HTTP_REFERER']
        return redirect(addr+'#'+str(comment_id))
    except:
        return redirect('/home')


@login_required(login_url='login')
def add_friend(request, user_id):
    user = User.objects.get(pk=user_id)
    me_user = request.user
    if BuddyList.objects.filter(owner_user=me_user,pure_members=user).exists():
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif BuddyList.objects.filter(owner_user=me_user, pending_users=user):
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif BuddyList.objects.filter(owner_user=me_user, i_send_to=user):
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif me_user==user:
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    else:
        BuddyList.add_to_send_to(me_user, user)
        BuddyList.add_to_pending(user, me_user)
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')


@login_required(login_url='login')
def cancel_request(request, user_id):
    user = User.objects.get(pk=user_id)
    me_user = request.user
    if BuddyList.objects.filter(owner_user=me_user,pure_members=user).exists():
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif BuddyList.objects.filter(owner_user=me_user,pending_users=user).exists():
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif me_user==user:
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    else:
        BuddyList.remove_from_send_to(me_user, user)
        BuddyList.remove_from_pending(user, me_user)
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')


@login_required(login_url='login')
def accept_request(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        me_user = request.user
    except:
        messages.error(request, 'Something went wrong.')
        return redirect('/home')

    if BuddyList.objects.filter(owner_user=me_user,pure_members=user).exists():
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif BuddyList.objects.filter(owner_user=me_user, i_send_to=user):
        messages.error(request, 'Something went wrong')
        return redirect('/home')
    elif me_user==user:
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    else:
        if BuddyList.objects.filter(owner_user=me_user,pending_users=user).exists():
            BuddyList.friend(me_user, user)
            BuddyList.friend(user, me_user)
            BuddyList.remove_from_pending(me_user, user)
            BuddyList.remove_from_send_to(user, me_user)
        else:
            messages.error(request, 'Something went wrong')
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')



@login_required(login_url='login')
def unfriend_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        me_user = request.user
    except:
        messages.error(request, 'Something went wrong.')
        return redirect('/home')

    if me_user==user:
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    
    if BuddyList.objects.filter(owner_user=me_user,pure_members=user).exists():
        BuddyList.unfriend(me_user, user)
        BuddyList.unfriend(user, me_user)
    else:
        messages.error(request, 'Something went wrong')

    try:
        addr = request.META['HTTP_REFERER']
        return redirect(addr)
    except:
        return redirect('/home')
    

@login_required(login_url='login')
def search_users(request):
    name = request.GET.get('query')
    if name=='' or name.isspace():
        messages.error(request, 'Something went wrong')
        try:
            addr = request.META['HTTP_REFERER']
            return redirect(addr)
        except:
            return redirect('/home')
    
    name = name.split(' ')[0]
    u = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
    data = {'users': u, 'fr':name}
    return render(request, 'user_stuff/search_page.html', data)


@login_required(login_url='login')
def notific(request):
    user = request.user
    try:
        qs = NotificationList.objects.get(owner_user=user)
        qs.number_of_new=0
        qs.save()
        qs = qs.my_notis.all().order_by('-date')
    except:
        qs = []
    
    return render(request, 'user_stuff/notific.html', {'data':qs})


@login_required(login_url='login')
def show_them(request, post_id):
    if request.method == 'GET':
        v = Post.objects.filter(pk=post_id)
        if v:
            curret_user = request.user
            post_user = v[0].user
            try:
                my_buddy_list = BuddyList.objects.get(owner_user=post_user)
                my_buddy_list = my_buddy_list.pure_members.all()
                
                if curret_user in my_buddy_list or curret_user==post_user:
                    try:
                        x = Love_Reaction.objects.get(post=v[0])
                        l = x.love_user.all()
                        c = x.cool_user.all()
                    except:
                        l= []
                        c=[]
                    return render(request, 'user_stuff/show_them.html', {'love_user': l, 'cool_user':c})
                else:
                    messages.error(request, "Something went wrong.")
                    return redirect('/home') 
            except:
                
                messages.error(request, "Something went wrong.")
                return redirect('/home')
        else:
            messages.error(request, "Post doesn't exists.")
            return redirect('/home')
    else:
        messages.error(request, "Something went wrong.")
        return redirect('/home')


@login_required(login_url='login')
def show_them2(request, comment_id):
    if request.method == 'GET':
        v = Comment.objects.filter(pk=comment_id)
        if v:
            curret_user = request.user
            comment_user = v[0].user
            try:
                my_buddy_list = BuddyList.objects.get(owner_user=comment_user)
                my_buddy_list = my_buddy_list.pure_members.all()
                
                if curret_user in my_buddy_list or curret_user==comment_user:
                    try:
                        x = Love_Reaction_On_Comment.objects.get(comment=v[0])
                        l = x.love_user.all()
                        c = x.cool_user.all()
                    except:
                        l= []
                        c=[]
                    return render(request, 'user_stuff/show_them.html', {'love_user': l, 'cool_user':c})
                else:
                    messages.error(request, "Something went wrong.")
                    return redirect('/home')
            except:
                messages.error(request, "Something went wrong.")
                return redirect('/home')
        else:
            messages.error(request, "Comment doesn't exists.")
            return redirect('/home') 
    else:
        messages.error(request, "Something went wrong.")
        return redirect('/home')


def activeers(request):
    x = User.objects.all()
    for i in x:
        if i.is_authenticated:
            print(i)

# def user_details_view(request):
#     return render(request, 'user_stuff/user_details_view.html')

@login_required(login_url='login')
def user_profile_see_more(request, username):
    user_ = User.objects.get(username=username)

    if request.user == user_:
        if request.method == 'GET':
            obj = User_Profile.objects.filter(user=user_)[0]
            return render(request, 'user_stuff/user_details_view.html', {"usr": user_, "other_user_flag":False})
        elif request.method == 'POST':
            pass
    else:
        return render(request, 'user_stuff/user_details_view.html', {"usr": user_, "other_user_flag":True})


@login_required(login_url='login')
def edit_user_profile_data(request, type, username):
    user_ = User.objects.get(username=username)
    data = User_Profile.objects.filter(user=user_)[0]
    type_ = type
    if request.method == 'GET':
        if user_ == request.user:
            if type == 1:
                type = "Bio"
                data = data.bio
            elif type == 2:
                type = "Hometown"
                data = data.hometown
            elif type == 3:
                type = "Current City"
                data = data.current_city
            elif type == 4:
                type = "Country"
                data = data.country
            elif type == 5:
                type = "Education"
                data = data.education
            elif type == 6:
                type = "Gender"
                data = data.gender
            elif type == 7:
                type = "Date of Birth"
                data = data.date_of_birth
            elif type == 8:
                type = "Relegion"
                data = data.religion
            elif type == 9:
                type = "About Me"
                data = data.about_me
            elif type == 10:
                type = "Favourite Quotes"
                data = data.favourite_quotes
            elif type == 11:
                type = "Relationship Status"
                data = data.relationship
            
            return render(request, 'user_stuff/edit_user_data_form.html', {"type": type_,"data": data, "usr":user_})
        else:
            messages.error(request, "Something went wrong.")
            return redirect('/home')
    elif request.method == 'POST':
        # 1 = bio
        # 2 = hometown
        # 3 = current_city
        # 4 = country
        # 5 = education
        # 6 = gender
        # 7 = date_of_birth
        # 8 = religion
        # 9 = about_me
        # 10 = fav_quotes
        # 11 = relationship
        data = request.POST['data']
        user_profile = User_Profile.objects.filter(user=user_)[0]
        if type == 1:
            user_profile.bio = data
            user_profile.save()
        elif type == 2:
            user_profile.hometown = data
            user_profile.save()
        elif type == 3:
            user_profile.current_city = data
            user_profile.save()
        elif type == 4:
            user_profile.country = data
            user_profile.save()
        elif type == 5:
            user_profile.education = data
            user_profile.save()
        elif type == 6:
            user_profile.gender = data
            user_profile.save()
        elif type == 7:
            user_profile.date_of_birth = data
            user_profile.save()
        elif type == 8:
            user_profile.religion = data
            user_profile.save()
        elif type == 9:
            user_profile.about_me = data
            user_profile.save()
        elif type == 10:
            user_profile.favorite_quotes = data
            user_profile.save()
        elif type == 11:
            user_profile.relationship = data
            user_profile.save()
        return render(request, 'user_stuff/user_details_view.html', {"usr": user_, "other_user_flag":False})


@login_required(login_url='login')
def message_box(request):
    user_ = request.user
    try:
        message_list_of_current_user = Message_List.objects.get(owner_user=user_)
        print(message_list_of_current_user.owner_user.username)
    except:
        return redirect('/home')


def message_someone(request, username_of_reciever):
    user_ = request.user
    # reciever = User.objects.filter(username= )

    if request.method == 'POST':
        # The message collected from the form
        # message_body = request.POST.get('message_body')
        # obj = All_messages(je_dise=user_, je_pabe=reciever, body=message_body)
        # obj.save()
        # Message_List.add(user=user_, another_user=reciever)
        # Message_List.add(user=reciever, another_user=user_)

        return render(request, 'user_stuff/individual_message.html', {})

    elif request.method == 'GET':
        return render(request, 'user_stuff/individual_message.html', {})
