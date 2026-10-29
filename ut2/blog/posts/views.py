from blog.comments.forms import AddCommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import AddPostForm
from .models import Post


@login_required
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


@login_required
def post_detail(request, post: Post):

    comment_form = AddCommentForm()
    context = {
        'post': post,
    }
    return render(request, 'posts/post/detail.html', {'post': post})


def add_post(request):
    if request.method == 'POST':
        if (form := AddPostForm(request.POST, request.FILES)).is_valid():
            post = form.save()
            return redirect(post)
            # return redirect('posts:post-list')
    else:
        form = AddPostForm()
    return render(request, 'posts/post/add.html', {'form': form, 'subtitle': 'Add Post'})


def add_comments(request, post_slug: str):
    post = Post.objects.get(slug=post_slug)
    if (form := AddCommentForm(request.POST)).is_valid():
        form.save(post, request.user)
    return redirect(post)


def delete_post(request, post: Post):
    post.delete()  # Pones esto pq el conversor que acabamos de crear ya lo buscamo y si no devuelve un error 404
    return redirect('posts:post-list')
