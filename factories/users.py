import factory

from users.models import Profile

from .auth import UserFactory


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    avatar = factory.django.ImageField(color=factory.Faker('color'))
    bio = factory.Faker('paragraph', nb_sentences=3)
