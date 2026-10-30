import factory
from django.utils import timezone
from faker import Faker

fake = Faker()

TZ = timezone.get_current_timezone()


class WaveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'waves.Wave'
        # Evita un save posterior y por lo tanto, evita que created_at y updated_at se sobreescriban
        skip_postgeneration_save = True

    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=100).replace('\n', ' '))
    user = factory.SubFactory('factories.auth.UserFactory')
    echo = factory.SubFactory('factories.echos.EchoFactory')

    @factory.post_generation
    def created_at(self, create, extracted, **kwargs):
        if not create:
            return
        value = extracted or fake.date_time_between(start_date=self.echo.created_at, tzinfo=TZ)
        # Avoid extra save
        self.__class__.objects.filter(pk=self.pk).update(created_at=value)
        self.created_at = value

    @factory.post_generation
    def updated_at(self, create, extracted, **kwargs):
        if not create:
            return
        value = extracted or fake.date_time_between(
            start_date=self.created_at + timezone.timedelta(hours=1),
            end_date=timezone.now(),
            tzinfo=TZ,
        )
        # Avoid extra save
        self.__class__.objects.filter(pk=self.pk).update(updated_at=value)
        self.updated_at = value
