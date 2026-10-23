from django.conf import settings
from django.db import models


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        'posts.Post',  # Modelo relacionado
        related_name='comments',  # Nombre relacionado
        on_delete=models.CASCADE,  # Acción de borrado
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


def __str__(self):
    return self.content
