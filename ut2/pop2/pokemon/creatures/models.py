from django.db import models


# Create your models here.
class Creature(models.Model):
    name = models.CharField(unique=True, max_length=256)
    slug = models.SlugField(unique=True, max_length=256)
    type1 = models.CharField(max_length=256)
    attack = models.PositiveIntegerField(default=0)
    defense = models.PositiveIntegerField(default=0)
    speed = models.PositiveIntegerField(default=0)
    generation = models.PositiveSmallIntegerField(default=1)


def __str__(self):
    return self.title
