from django import forms
from django.utils.text import slugify

from .models import Post


class AddPostForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    published_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    title.widget.attrs.update({'id': 'post-title'})
    content.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):

        post = super().save(commit=False)

        post.slug = slugify(post.title)

        post = super().save(*args, **kwargs)

        return post


from django import forms

from .models import Post


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
