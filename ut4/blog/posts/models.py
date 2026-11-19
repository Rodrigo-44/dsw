from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .validators import cacharacter_post, validate_title


class PostLabelingDetail(models.Model):
    post = models.ForeignKey(
        'posts.Post',
        related_name='post_labeling_details',
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey(
        'labels.Label',
        related_name='post_labeling_details',
        on_delete=models.CASCADE,
    )
    reason = models.CharField(max_length=256)
    labeled_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    DEFAULT_RANK = 3

    class Category(models.TextChoices):
        SOCIETY = 'SOC', 'Society'
        EDUCATION = 'EDU', 'Education'
        HEALTH = 'HLT', 'Health'
        CULTURE = 'CUL', 'Culture'
        TECH = 'TEC', 'Technology'

    class Rating(models.IntegerChoices):
        VERY_BAD = 1
        BAD = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5

    title = models.CharField(max_length=256, validators=[validate_title])
    slug = models.SlugField(max_length=256, unique=True)
    content = models.TextField(validators=[cacharacter_post])
    published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='covers',
        default='covers/nocover.png',
    )
    category = models.CharField(
        max_length=3,
        choices=Category,
        default=Category.SOCIETY,
    )
    rating = models.IntegerField(
        choices=Rating,
        default=Rating.AVERAGE,
    )
    labels = models.ManyToManyField(
        'labels.Label',
        related_name='posts',
        through='posts.PostLabelingDetail',
        blank=True,
    )
    rank = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=DEFAULT_RANK,
    )

    # -created_ad
    class Meta:
        ordering = ['title']
        unique_together = ['title', 'slug']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self])

    @property
    def rating_color(self) -> str:
        VERY_BAD_COLOR = 'FF6347'
        BAD_COLOR = '654321'
        AVERAGE_COLOR = 'EDD84F'
        GOOD_COLOR = '365A6E'
        EXCELLENT_COLOR = '528532'
        NO_RATING_COLOR = '000000'

        match self.rating:
            case self.Rating.VERY_BAD:
                color = VERY_BAD_COLOR
            case self.Rating.BAD:
                color = BAD_COLOR
            case self.Rating.AVERAGE:
                color = AVERAGE_COLOR
            case self.Rating.GOOD:
                color = GOOD_COLOR
            case self.Rating.EXCELLENT:
                color = EXCELLENT_COLOR
            case _:
                color = NO_RATING_COLOR
        return f'#{color}'

    def clean(self):
        if self.slug != slugify(self.title):
            raise ValidationError("Slug does not match with title's slugify")
    
    def content_label(self):
        