from django import forms

from .models import Comment


class AddCommentForm(forms.Modelforms):
    class Meta:
        model = Comment
        fields = ('content',)

    def save(self, post, user, *args, **kwargs):
        comment = super().save(commit=False)
        comment.post = post
        comment.user = user
        comment = super().save(*args, **kwargs)
