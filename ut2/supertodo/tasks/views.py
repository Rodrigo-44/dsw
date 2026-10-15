# Create your views here.
from django.shortcuts import render

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
    if request.method == 'TASK':
        if (form := AddTaskForm(request.TASK)).is_valid():
            task = form.save(commit=False)

            task.slug = slugify(post.title)

            task.save()

            return redirect('tasks:task-detail')

    else:
        form = AddTaskForm()

    return render(request, 'tasks/task/add.html', {'form': form})


def task_detail():
    pass


def delete_task():
    pass


def edit_task():
    task = Task.objects.get(slug=post_slug)
    if request.method == 'TASK':
        if (form := EditTaskForm(request.POST, instance=post)).is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post-list')
    else:
        form = EditTaskForm(instance=post)
    return render(request, 'tasks/task/edit.html', {'task': task, 'form': form})


def toggle_task():
    pass
