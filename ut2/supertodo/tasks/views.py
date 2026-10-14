# Create your views here.
from django.shortcuts import render

from .models import Task


def task_list(request):
    tasks = Task.objects.order_by('-created_at')
    total_tasks = tasks.count()
    return render(request, 'tasks/task/list.html', {'tasks': tasks, 'total_tasks': total_tasks})


def task_list_pending(request):
    pending_list = Task.objects.filter(completed__lt=1)
    total_tasks = pending_list.count()
    return render(
        request,
        'tasks/task/pending.html',
        {'pending_list': pending_list, 'total_tasks': total_tasks},
    )


def task_list_completed(request):
    completed_list = Task.objects.filter(completed__gt=0)
    total_tasks = completed_list.count()
    return render(
        request,
        'tasks/task/completed.html',
        {'completed_list': completed_list, 'total_tasks': total_tasks},
    )


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
