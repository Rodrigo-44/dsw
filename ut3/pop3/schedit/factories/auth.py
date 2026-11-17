import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .extras import UniqueFaker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = UniqueFaker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda obj: f'{slugify(obj.first_name)}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.django.Password('1234')
