from django import forms
from django.utils.text import slugify

from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

    def save(self, *args, **kwargs):
        post = super().save(commit=False)
        post.slug = slugify(post.title)
        post = super().save(*args, **kwargs)
        return post
