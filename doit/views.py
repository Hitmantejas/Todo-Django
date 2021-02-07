from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import DoitForm
from .models import Doit
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'doit/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'doit/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentdoits')
            except IntegrityError:
                return render(request, 'doit/signupuser.html',{'form': UserCreationForm(), 'error': 'This Username is already taken. Please try another.'})

        else:
            return render(request, 'doit/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords Did Not Match.'})
            # print("Passwords does not match")


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'doit/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'doit/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('currentdoits')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createdoits(request):
    if request.method == 'GET':
        return render(request, 'doit/createdoits.html', {'form': DoitForm()})
    else:
        try:
            form = DoitForm(request.POST)
            newdoit = form.save(commit=False)
            newdoit.user = request.user
            newdoit.save()
            return redirect('currentdoits')
        except ValueError:
            return render(request, 'doit/createdoits.html', {'form': DoitForm(), 'error': 'Title can not be more than 100 characters'})


@login_required
def currentdoits(request):
    doits = Doit.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'doit/currentdoits.html', {'doits': doits})


@login_required
def completed(request):
    doits = Doit.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'doit/completed.html', {'doits': doits})


@login_required
def viewdoit(request, doit_pk):
    doit = get_object_or_404(Doit, pk=doit_pk, user=request.user)
    if request.method == 'GET':
        form = DoitForm(instance=doit)
        return render(request, 'doit/viewdoit.html', {'doit': doit, 'form': form})
    else:
        try:
            form = DoitForm(request.POST, instance=doit)
            form.save()
            return redirect('currentdoits')
        except ValueError:
            return render(request, 'doit/viewdoit.html', {'doit': doit, 'form': form, 'error':'Bad Input.Please Try Again.'})


@login_required
def completedoit(request, doit_pk):
    doit = get_object_or_404(Doit, pk=doit_pk, user=request.user)
    if request.method == 'POST':
        doit.datecompleted = timezone.now()
        doit.save()
        return redirect('currentdoits')


@login_required
def deletedoit(request, doit_pk):
    doit = get_object_or_404(Doit, pk=doit_pk, user=request.user)
    if request.method == 'POST':
        doit.delete()
        return redirect('currentdoits')