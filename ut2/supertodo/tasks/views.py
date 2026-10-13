# Create your views here.
from django.shortcuts import render

from .models import Task


def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    total_tasks = tasks.count()
    return render(request, 'tasks/task/list.html', {'tasks': tasks, 'total_tasks': total_tasks})


def task_list_pending():
    pass


def task_list_completed():
    pass


def add_task():
    pass


def task_detail():
    pass


def delete_task():
    pass


def edit_task():
    pass


def toggle_task():
    pass
