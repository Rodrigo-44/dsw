from django import forms

from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'cover')

    # def save(self, *args, **kwargs):
    #   post = super().save(commit=False)
    #  post.slug = slugify(post.title)
    # post = super().save(*args, **kwargs)
    # return post
