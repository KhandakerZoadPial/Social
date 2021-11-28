from django.shortcuts import render, HttpResponse as HR, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from user_stuff.models import User_Profile


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/home')
    return render(request, 'account/signup.html')


def signup(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already have an account.')
        return redirect('/home')
    if request.method == 'POST':
        mail = request.POST.get('email', '')
        username = request.POST.get('username', '')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('confpass', '')

        if mail=='' or username=='' or password1=='' or password2=='' or fname=='' or lname=='':
            messages.error(request, 'No field can be left empty.')
            return redirect('signup')


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Taken.')
                return redirect('signup')
            elif User.objects.filter(email=mail).exists():
                messages.error(request, 'Email Already Taken.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=mail, first_name=fname, last_name=lname)
                user.save()
                x = User_Profile(user=user)
                x.save()
                messages.success(request, 'Wellcome to Social. Be Social! Go..!')
                return redirect('/login')

    return redirect('/')


def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in.')
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if username=='' or password=='':
            messages.error(request, 'Username or password cannot be empty!Please try again.')
            return redirect('/login')

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('/home')
        else:
            messages.error(request, 'Please provide valid credentials!')
            return redirect('/login')
    else:
        return render(request, 'account/login.html')


@login_required(login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('/login')
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('/login')
