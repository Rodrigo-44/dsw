from django.conf import settings
from django.db import models
from django.urls import reverse


class Wave(models.Model):
    content = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='waves', on_delete=models.CASCADE
    )
    echo = models.ForeignKey('echos.echo', related_name='waves', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('echos:echo-detail', args=[self.echo.pk])

    def __str__(self):
        return f'{self.content}, {self.user}, {self.created_at}'
