from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #valida error del nombre de usuario, el cual es unico. Si se repite tira el error.
# Create your views here.

def index(request):
    return render (request, 'index.html')

def signup(request):
    if request.method=='GET':
        return render (request, 'signup.html',{
        'form':UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
            #se registra usuario
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user) #coloca un sessionid en las cookies
                return redirect('tasks') #termina aca y visualisa tasks
            except IntegrityError:
                return render (request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'Username already exists'
                })

        return render (request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'Password does not match'
                })

def tasks (request):
    return render (request,'tasks.html')

def logging_out(request):
    logout(request)
    return redirect ('index')

def signin(request):
    if request.method=='GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
    })
    else:
        print(request.POST)
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Incorrect username or password. Try again.'
        })
        else:
            login(request,user) #coloca un sessionid en las cookies
            return redirect ('tasks')
