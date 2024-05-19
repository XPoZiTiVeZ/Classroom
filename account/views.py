from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_user
from django.contrib.auth import login as login_user
from django.contrib import messages
from .backends import Backend
from .models import User
from uuid import uuid4


def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            

            if username == "" and username is not None:
                messages.error(request, 'Имя пользователя не указано.')
                return redirect('register')
            
            if email == "" and email is not None:
                messages.error(request, 'Электронная почта не указана.')
                return redirect('register')
            
            if password == "" and password is not None:
                messages.error(request, 'Пароль не указан.')
                return redirect('register')
            
            if password != password2:
                messages.error(request, 'Пароли не совпадают.')
                return redirect('register')

            user = User.objects.create_user(uuid=uuid4().hex, username=username, email=email, password=password)
            user.save()
            login_user(request, user, 'account.backends.Backend')

            return redirect('home')

        return render(request, 'account/register.html')
    
    return redirect('home')

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = Backend().authenticate(request, username, password)
            if user is None:
                messages.error(request, 'Неправильная почта или пароль')
                return redirect('login')
            
            login_user(request, user, 'account.backends.Backend')
            messages.success(request, f'Добро пожаловать, {user.username}')

            next = request.GET.get('next', None)
            if next is not None:
                return redirect(next)

            return redirect('home')
        
        return render(request, 'account/login.html')
    
    return redirect('home')

def logout(request):
    logout_user(request)
    return redirect('login')

def profile(request, user_uuid=None, username=None, email=None):
    if request.method == "GET":
        return render(request, "account/profile.html")
    elif request.method == "POST":
        pass

def set_password(request):  
    if request.method == "POST":
         return render(request, "course/index.html")
    return render(request, "account/set_password.html")