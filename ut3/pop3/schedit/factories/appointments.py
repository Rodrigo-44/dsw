from datetime import date, timedelta

import factory

from appointments.models import Appointment

from .auth import UserFactory
from .slots import SlotFactory


class AppointmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Appointment

    user = factory.SubFactory(UserFactory)
    slot = factory.SubFactory(SlotFactory)

    @factory.lazy_attribute_sequence
    def date(self, n):
        add_days = n // 9 + 1
        return date.today() + timedelta(days=add_days)
