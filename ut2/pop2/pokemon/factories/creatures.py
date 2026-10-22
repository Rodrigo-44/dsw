import factory
from django.utils.text import slugify

from creatures.models import Creature

from . import pokemon


class CreatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Creature

    name = factory.Iterator(pokemon.NAMES)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    type1 = factory.Iterator(t.upper() for t in pokemon.TYPES)
    attack = factory.Faker('random_int', min=10, max=200)
    defense = factory.Faker('random_int', min=10, max=200)
    speed = factory.Faker('random_int', min=10, max=200)
    generation = factory.Faker('random_int', min=1, max=8)
