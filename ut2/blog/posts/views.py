from django.shortcuts import redirect, render

from .forms import AddPostForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    author = f'{request.user.first_name} {request.user.last_name}'
    return render(
        request,
        'posts/post/list.html',
        {
            'subtitle': 'Todos los posts',
            'posts': posts,
            'author': author,
        },
    )


def post_detail(request, post_slug: str):
    post = Post.objects.get(slug=post_slug)
    return render(request, 'posts/post/detail.html', {'post': post})


def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST)).is_valid():
            form.save()
            return redirect('posts:post-list')
    else:
        form = AddPostForm()
    return render(request, 'posts/post/add.html', {'form': form, 'subtitle': 'Add Post'})
