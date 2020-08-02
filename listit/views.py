from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ItemForm
from .models import Item
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def currentlistit(request):
    items = Item.objects.filter(user=request.user, completed_at__isnull=True)
    return render(request, 'listit/currentlistit.html', {'items':items})

@login_required
def completedlistit(request):
    items = Item.objects.filter(user=request.user, completed_at__isnull=False).order_by('-completed_at')
    return render(request, 'listit/completedlistit.html', {'items':items})

@login_required
def createitem(request):
    if request.method == 'GET':
        return render(request, 'listit/createitem.html', {'form':ItemForm()})
    else:
        try:
            form = ItemForm(request.POST)
            newItem = form.save(commit=False)
            newItem.user = request.user
            newItem.save()
            return redirect('currentlistit')
        except ValueError:
            return render(request, 'listit/createitem.html', {'form':ItemForm(), 'error':'Bad data passed in. Try again'})

@login_required
def viewitem(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'GET':
        form = ItemForm(instance=item)
        return render(request, 'listit/viewitem.html', {'item':item, 'form':form})
    else:
        try:
            form = ItemForm(request.POST, instance=item)
            form.save()
            return redirect('currentlistit')
        except ValueError:
            return render(request, 'listit/viewitem.html', {'item':item, 'form':form, 'error':'Bad information'})

@login_required
def completeitem(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'POST':
        item.completed_at = timezone.now()
        item.save()
        return redirect('currentlistit')

@login_required
def deleteitem(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('currentlistit')