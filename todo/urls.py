from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create/', create, name='create'),
    path('todo/<int:todo_id>/', showTodo, name='showtodo'),
    path('completeTodo/<int:todo_id>/complete', completeTodo, name='completeTodo'),
    path('completetodos/', completetodos, name='completetodos'),
    path('complete_to_todo/<int:todo_id>/', complete_to_todo, name='complete_to_todo'),
    path('delete_todos/<int:todo_id>/', delete_todos, name='delete_todos'),
    path('update_todo/<int:todo_id>/', update_todo, name='update_todo'),
]