# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import AddTaskForm, EditTaskForm
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


def add_task(request):
    if request.method == 'POST':
        if (form := AddTaskForm(request.TASK)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:task-detail')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/task/add.html', {'form': form})


def task_detail(request, task_slug: str):
    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        return HttpResponse(f'La tarea con slug {task_slug} no existe.')
    return render(request, 'tasks/task/detail.html', {'task': task})


def delete_task(request, task_slug: str):
    task = Task.objects.filter(slug__contains=task_slug)
    task.delete()
    return render(request, 'tasks/task/delete.html', {'task': task})


def edit_task(request, task_slug: str):
    task = Task.objects.get(slug=task_slug)
    if request.method == 'POST':
        if (form := EditTaskForm(request.POST, instance=task)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:task-list')
    else:
        form = EditTaskForm(instance=task)
    return render(request, 'tasks/task/edit.html', {'task': task, 'form': form})


def toggle_task(request, task_slug=str):
    task = Task.objects.get(slug=task_slug)
    task.completed = not task.completed
    task.save()
    return redirect('tasks:task-list')
