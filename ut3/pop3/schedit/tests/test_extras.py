import datetime

import pytest

from appointments.models import Appointment
from factories import AppointmentFactory, SlotFactory
from slots.models import Slot

from . import conftest

# ==============================================================================
# SLOT
# ==============================================================================


def test_str_representation_of_slot():
    slot = SlotFactory.build(start_at=datetime.time(17, 0), end_at=datetime.time(17, 0))
    assert str(slot) == '17:00 - 17:00', (
        'La representación en cadena de texto del modelo Slot no es correcta.'
    )


def test_default_ordering_of_slot_model():
    assert Slot._meta.ordering == ['start_at', 'end_at'], (
        'La configuración de ordenación del modelo Slot no es correcta.'
    )


# ==============================================================================
# APPOINTMENT
# ==============================================================================


def test_default_ordering_of_appointment_model():
    assert Appointment._meta.ordering == ['date', 'slot'], (
        'La configuración de ordenación del modelo Appointment no es correcta.'
    )


def test_str_representation_of_appointment():
    slot = SlotFactory.build(start_at=datetime.time(16, 0), end_at=datetime.time(17, 0))
    appointment = AppointmentFactory.build(date=datetime.date(2024, 9, 21), slot=slot)
    assert str(appointment) == '2024-09-21 (16:00 - 17:00)', (
        'La representación en cadena de texto del modelo Appointment no es correcta.'
    )


@pytest.mark.django_db
def test_appointment_object_has_get_absolute_url_method(appointment):
    expected_url = conftest.APPOINTMENT_DETAIL_URL.format(appointment_pk=appointment.pk)
    assert appointment.get_absolute_url() == expected_url
