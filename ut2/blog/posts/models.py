from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, editable=False)
    content = models.TextField()
    published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='covers',
        default='covers/nocover.png',
    )

    # -created_ad
    class Meta:
        ordering = ['title']

    class Meta:
        unique_together = ['title', 'slug']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self.slug])
