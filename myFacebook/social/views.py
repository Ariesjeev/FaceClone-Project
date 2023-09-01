#from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from .models import UserPost

def index(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST['username']
            pwd = request.POST['password']
            user = authenticate(username=username, password=pwd)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        return redirect('home')
    return render(request, 'index.html')

@login_required(login_url='index')
def home(request):
    user = request.user
    context = {'user': user}
    posts = UserPost.objects.all()
    context.update({"posts": posts})
    return render(request, 'home.html', context)

@login_required(login_url='index')
def profile(request):
    user = request.user
    context = {'user': user}
    posts = UserPost.objects.filter(user=user)
    context.update({"posts": posts})
    return render(request, 'profile.html', context)

def signout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = User.objects.create(username=username)
        user.set_password(pwd)
        user.save()
        return redirect('index')
    return redirect('index')

def update_profile(request):
    if request.method == 'POST':
        status = request.POST['status']
        loc = request.POST['location']
        user_profile = request.user.userprofile
        if len(status) == 0 and len(loc) != 0:
            user_profile.loc = loc
        elif len(loc) == 0 and len(status) != 0:
            user_profile.bio = status
        elif len(status) > 0 and len(loc) > 0:
            user_profile.loc = loc
            user_profile.bio = status
        user_profile.save()
    return redirect('profile')

def create_post(request):
    if request.method == 'POST':
        content = request.POST['content']
        if len(content) > 0:
            post = UserPost.objects.create(user=request.user, post=content)
            post.save()
    return redirect('home')
