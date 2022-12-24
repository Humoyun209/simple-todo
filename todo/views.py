import datetime
import time
from datetime import date, timedelta

from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RegisterUserForm, UserLoginForm, CreateToDo
from .models import Todo


def index(request):
    todos = Todo.objects.filter(user_id=request.user.id, date_completed__isnull=True)
    context = {
        'todos': todos,
        'title': 'home'
    }
    return render(request, 'todo/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка при регистрации')
    else:
        form = RegisterUserForm(request.POST)
    return render(request, 'todo/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка при авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'todo/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def create(request):
    if request.method == 'POST':
        form = CreateToDo(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Вы успешно добавили todo')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка')

    else:
        form = CreateToDo()
    return render(request, 'todo/create.html', {'form': form})


def showTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    context = {
        'todo': todo,
        'title': f'todo-{todo_id}'
    }
    return render(request, 'todo/showTodo.html', context=context)


def completeTodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('index')


def completetodos(request):
    today = date.today()
    yesterday = today - timedelta(days=1)
    now = datetime.datetime.now()
    todos = Todo.objects.filter(user_id=request.user.id, date_completed__isnull=False, date_completed__gte=yesterday)
    context = {
        'todos': todos,
        'title': 'completed'
    }
    print(yesterday)
    print(now)
    return render(request, 'todo/comptodos.html', context=context)


def complete_to_todo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if request.method == 'POST':
        todo.date_completed = None
        todo.save()
        return redirect('index')


def delete_todos(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    # todo = Todo.objects.get(pk=todo_id)
    if request.method == 'POST':
        todo.delete()
        return redirect('index')


def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'GET':
        form = CreateToDo(instance=todo)
        return render(request, 'todo/updatetodo.html', {'form': form})
    if request.method == 'POST':
        form = CreateToDo(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully change')
            return redirect('index')
        else:
            messages.error(request, 'Error input')
    else:
        form = CreateToDo(instance=todo)
    return render(request, 'todo/updatetodo.html', {'form': form})