import factory
from django.utils.text import slugify
from faker import Faker

from tasks.models import Task

fake = Faker()


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
        django_get_or_create = ('slug',)

    name = factory.LazyFunction(lambda: fake.unique.sentence(nb_words=4).rstrip('.'))
    description = factory.Faker('paragraph', nb_sentences=3)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    completed = factory.Faker('boolean', chance_of_getting_true=30)
