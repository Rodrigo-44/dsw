import pytest
from django.conf import settings

from tasks.models import Task

# ==============================================================================
# Required Apps
# ==============================================================================


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('tasks', 'shared')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(PROPER_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


# ==============================================================================
# Task Model
# ==============================================================================


@pytest.mark.score(2)
@pytest.mark.django_db
def test_task_model_is_correctly_configured():
    # name
    assert (f := Task._meta.get_field('name')), 'Task.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Task.name no tiene el tipo esperado'
    assert not f.blank, 'Task.name no debe admitir valores en blanco'

    # slug
    assert (f := Task._meta.get_field('slug')), 'Task.slug no se ha definido'
    assert f.get_internal_type() == 'SlugField', 'Task.slug no tiene el tipo esperado'
    assert f.unique, 'Task.slug no se ha definido como único'
    assert not f.blank, 'Task.slug no debe admitir valores en blanco'

    # description
    assert (f := Task._meta.get_field('description')), 'Task.description no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Task.description no tiene el tipo esperado'
    assert f.blank, 'Task.description no permite valores en blanco'

    # completed
    assert (f := Task._meta.get_field('completed')), 'Task.completed no se ha definido'
    assert f.get_internal_type() == 'BooleanField', 'Task.completed no tiene el tipo esperado'
    assert not f.default, 'Task.completed no tiene el valor por defecto esperado'
    assert not f.blank, 'Task.completed no debe admitir valores en blanco'

    # created_at
    assert (f := Task._meta.get_field('created_at')), 'Task.created_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Task.created_at no tiene el tipo esperado'

    # updated_at
    assert (f := Task._meta.get_field('updated_at')), 'Task.updated_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Task.updated_at no tiene el tipo esperado'
    assert f.auto_now, 'Task.updated_at no tiene auto_now=True'
