from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import AddPostForm, EditPostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(
        request,
        'posts/post/list.html',
        {
            'subtitle': 'Todos los posts',
            'posts': posts,
        },
    )


def post_detail(request, post_slug: str):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'posts/post/detail.html', {'post': post})


def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST)).is_valid():
            post = form.save(commit=False)

            post.slug = slugify(post.title)

            post.save()

            return redirect('posts:post-list')

    else:
        form = AddPostForm()

    return render(request, 'posts/post/add.html', {'form': form})


def edit_post(request, post_slug: str):
    post = Post.objects.get(slug=post_slug)
    if request.method == 'POST':
        if (form := EditPostForm(request.POST, instance=post)).is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts:post-list')
    else:
        form = EditPostForm(instance=post)
    return render(request, 'posts/post/edit.html', {'post': post, 'form': form})


def change_post_status(request, post_slug: str, post_private: bool):

    try:
        post = Post.objects.get(slug=post_slug)
        post.private = post_private
        post.save()
    except Post.DoesNotExist:
        return HttpResponse('Post does not exist')
