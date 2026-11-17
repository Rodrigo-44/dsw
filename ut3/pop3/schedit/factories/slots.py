import datetime

import factory

from slots.models import Slot


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Slot
        django_get_or_create = ('start_at', 'end_at')

    @factory.sequence
    def start_at(n):
        STARTING_HOUR = 8
        ENDING_HOUR = 17
        hour = STARTING_HOUR + (n % (ENDING_HOUR - STARTING_HOUR))
        return datetime.time(hour, 0)

    @factory.lazy_attribute
    def end_at(self):
        start_hour = self.start_at.hour
        end_hour = start_hour + 1
        return datetime.time(end_hour, 0)
