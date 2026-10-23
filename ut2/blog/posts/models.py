from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True)
    content = models.TextField()
    published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='covers',
        default='covers/nocover.png',
    )

    def __str__(self):
        return self.title
