import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from appointments.models import Appointment
from slots.models import Slot

User = get_user_model()


def test_required_apps_are_installed():
    REQUIRED_APPS = ('accounts', 'slots', 'appointments')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in REQUIRED_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(REQUIRED_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


# ==============================================================================
# SLOT
# ==============================================================================


@pytest.mark.score(2)
def test_slot_model_is_correctly_configured():
    # start_at field
    assert (f := Slot._meta.get_field('start_at')), 'Slot.start_at no se ha definido'
    assert f.get_internal_type() == 'TimeField', 'Slot.start_at no es del tipo esperado'
    assert not f.unique, 'Slot.start_at no debe ser un campo único (por sí solo)'
    assert not f.auto_now, 'Slot.start_at no debe tener auto_now activado'
    assert not f.auto_now_add, 'Slot.start_at no debe tener auto_now_add activado'
    assert not f.blank, 'Slot.start_at no debe admitir valores en blanco'

    # end_at field
    assert (f := Slot._meta.get_field('end_at')), 'Slot.end_at no se ha definido'
    assert f.get_internal_type() == 'TimeField', 'Slot.end_at no es del tipo esperado'
    assert not f.unique, 'Slot.end_at no debe ser un campo único (por sí solo)'
    assert not f.auto_now, 'Slot.end_at no debe tener auto_now activado'
    assert not f.auto_now_add, 'Slot.end_at no debe tener auto_now_add activado'
    assert not f.blank, 'Slot.end_at no debe admitir valores en blanco'

    # Meta options
    assert Slot._meta.unique_together == (('start_at', 'end_at'),), (
        'La configuración de claves únicas juntas del modelo Slot no es correcta.'
    )


# ==============================================================================
# APPOINTMENT
# ==============================================================================


@pytest.mark.score(2)
def test_appointment_model_is_correctly_configured():
    # date field
    assert (f := Appointment._meta.get_field('date')), 'Appointment.date no se ha definido'
    assert f.get_internal_type() == 'DateField', 'Appointment.date no es del tipo esperado.'
    assert not f.unique, 'Appointment.date no debe ser un campo único (por sí solo).'
    assert not f.auto_now, 'Appointment.date no debe tener auto_now activado.'
    assert not f.auto_now_add, 'Appointment.date no debe tener auto_now_add activado.'
    assert not f.blank, 'Appointment.date no debe admitir valores en blanco'

    # user field
    assert (f := Appointment._meta.get_field('user')), 'Appointment.user no se ha definido.'
    assert f.get_internal_type() == 'ForeignKey', 'Appointment.user no es del tipo esperado.'
    assert f.remote_field.model == User, 'Appointment.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Appointment.user no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'appointments', (
        'Appointment.user no tiene el related_name esperado.'
    )
    assert not f.blank, 'Appointment.user no debe admitir valores en blanco'

    # slot field
    assert (f := Appointment._meta.get_field('slot')), 'Appointment.slot no se ha definido.'
    assert f.get_internal_type() == 'ForeignKey', 'Appointment.slot no es del tipo esperado.'
    assert f.remote_field.model == Slot, 'Appointment.slot no referencia al modelo esperado.'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Appointment.slot no tiene el método de borrado esperado.'
    )
    assert f.remote_field.related_name == 'appointments', (
        'Appointment.slot no tiene el related_name esperado.'
    )
    assert not f.unique, 'Appointment.slot no debe ser un campo único (por sí solo).'
    assert not f.blank, 'Appointment.slot no debe admitir valores en blanco.'

    # Meta options
    assert Appointment._meta.unique_together == (('date', 'slot'),), (
        'La configuración de claves únicas juntas del modelo Appointment no es correcta.'
    )
