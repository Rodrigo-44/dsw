import factory
from django.utils import timezone
from faker import Faker

from .extras import RelatedFactoryVariableList

fake = Faker()

TZ = timezone.get_current_timezone()


class EchoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'echos.Echo'
        # Evita un save posterior y por lo tanto, evita que created_at y updated_at se sobreescriban
        skip_postgeneration_save = True

    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=300).replace('\n', ' '))
    user = factory.SubFactory('factories.auth.UserFactory')

    @factory.post_generation
    def created_at(self, create, extracted, **kwargs):
        if not create:
            return
        value = extracted or fake.date_time_this_year(tzinfo=TZ)
        # Avoid extra save
        self.__class__.objects.filter(pk=self.pk).update(created_at=value)
        self.created_at = value

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create:
            return
        value = extracted or fake.date_time_between(
            start_date=self.created_at + timezone.timedelta(hours=1), tzinfo=TZ
        )
        # Avoid extra save
        self.__class__.objects.filter(pk=self.pk).update(updated_at=value)
        self.updated_at = value


class EchoRelatedFactory(EchoFactory):
    waves = RelatedFactoryVariableList(
        'factories.waves.WaveFactory', factory_related_name='echo', size=5
    )
