from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError #valida error del nombre de usuario, el cual es unico. Si se repite tira el error.
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def tasks (request):
    tasks=Task.objects.filter(user=request.user,date_completed__isnull=True) #muestra tareas segun usuario y si datecompleted es falso o no ha sido completada
    return render (request,'tasks.html',{'tasks':tasks})

@login_required
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

@login_required
def create_task(request):
    if request.method=='GET':
        return render(request,'createtask.html',{
            'form':CreateTaskForm
        })
    else:
        try:
            form=CreateTaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request,'createtask.html',{
            'form':CreateTaskForm,
            'error':'Error, try again.'
        })

@login_required
def read_task(request,task_id):
    if request.method == 'GET':
        task=get_object_or_404(Task,pk=task_id, user=request.user)# solicito el modelo Task y busca el dato donde el pk sea igual a task_id Y si no esta tira error 404
        form = CreateTaskForm(instance=task)
        return render (request,'readtask.html',{
            'task':task,
            'form':form
        })
    else:
        try:
            task = get_object_or_404(Task,pk=task_id, user=request.user)# debe ser el mismo usuario que creo el que pueda modificarlo.
            form = CreateTaskForm(request.POST,instance=task) #toma los datos de las tareas y genera un nuevo formulario
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request,'readtask.html',{
            'task':task,
            'form':form,
            'error': 'There was an error updating your task. Try again.'
        })

@login_required
def task_completed(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.delete()
        return redirect('tasks')

@login_required
def all_tasks_completed (request):
    tasks=Task.objects.filter(user=request.user,date_completed__isnull=False).order_by('date_completed') 
    return render (request,'tasks.html',{'tasks':tasks})