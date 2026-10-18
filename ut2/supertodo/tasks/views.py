# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import AddTaskForm, EditTaskForm
from .models import Task


def task_list(request):
    return _render_task_list(request, Task.objects.all(), 'Todas las tareas')


def task_list_pending(request):
    return _render_task_list(
        request, Task.objects.filter(completed=False), 'Tareas pendientes'
    )


def task_list_completed(request):
    return _render_task_list(
        request, Task.objects.filter(completed=True), 'Tareas completadas'
    )


def _render_task_list(request, tasks, subtitle):
    tasks = tasks.order_by('-created_at')
    return render(
        request,
        'tasks/task/list.html',
        {'tasks': tasks, 'total_tasks': tasks.count(), 'subtitle': subtitle},
    )


def add_task(request):
    if request.method == 'POST':
        if (form := AddTaskForm(request.POST)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:task-list')
    else:
        form = AddTaskForm()
    return render(
        request,
        'tasks/task/add.html',
        {'form': form, 'subtitle': 'Añadir tarea'},
    )


def task_detail(request, task_slug: str):
    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        return HttpResponse(f'La tarea con slug "{task_slug}" no existe.')
    return render(request, 'tasks/task/detail.html', {'task': task})


def delete_task(request, task_slug: str):
    task = get_object_or_404(Task, slug=task_slug)
    task.delete()
    return redirect('tasks:task-list')


def edit_task(request, task_slug: str):
    task = get_object_or_404(Task, slug=task_slug)
    if request.method == 'POST':
        if (form := EditTaskForm(request.POST, instance=task)).is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.name)
            task.save()
            return redirect('tasks:task-detail', task_slug=task.slug)
    else:
        form = EditTaskForm(instance=task)
    return render(
        request,
        'tasks/task/edit.html',
        {'task': task, 'form': form, 'subtitle': 'Editar tarea'},
    )


def toggle_task(request, task_slug=str):
    task = get_object_or_404(Task, slug=task_slug)
    task.completed = not task.completed
    task.save()
    return redirect('tasks:task-list')
