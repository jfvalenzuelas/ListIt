from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    return render(request, 'listit/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'listit/signupuser.html', {'form':UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentlistit')
            except IntegrityError:
                return render(request, 'listit/signupuser.html', {'form':UserCreationForm(), 'error':'Username already exists'})
        else:
            # Password did not match
            return render(request, 'listit/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords do not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'listit/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'listit/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentlistit')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currentlistit(request):
    return render(request, 'listit/currentlistit.html')
