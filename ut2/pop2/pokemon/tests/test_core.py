import pytest
from django.conf import settings

from creatures.models import Creature


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('creatures', 'shared')

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
# Creature Model
# ==============================================================================


@pytest.mark.score(2)
def test_creature_model_is_correctly_configure():
    # name
    assert (f := Creature._meta.get_field('name')), 'Creature.name no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Creature.name no es del tipo esperado'
    assert f.unique, 'Creature.name no se ha definido como único'
    assert not f.blank, 'Creature.name no debe admitir valores en blanco'

    # slug
    assert (f := Creature._meta.get_field('slug')), 'Creature.slug no se ha definido'
    assert f.get_internal_type() == 'SlugField', 'Creature.slug no es del tipo esperado'
    assert f.unique, 'Creature.slug no se ha definido como único'
    assert not f.blank, 'Creature.slug no debe admitir valores en blanco'

    # type1
    assert (f := Creature._meta.get_field('type1')), 'Creature.type1 no se ha definido'
    assert f.get_internal_type() == 'CharField', 'Creature.type1 no es del tipo esperado'
    assert not f.blank, 'Creature.type1 no debe admitir valores en blanco'

    # attack
    assert (f := Creature._meta.get_field('attack')), 'Creature.attack no se ha definido'
    assert f.get_internal_type() == 'PositiveIntegerField', (
        'Creature.attack no es del tipo esperado'
    )
    assert f.default == 0, 'Creature.attack no tiene el valor por defecto esperado'
    assert not f.blank, 'Creature.attack no debe admitir valores en blanco'

    # defense
    assert (f := Creature._meta.get_field('defense')), 'Creature.defense no se ha definido'
    assert f.get_internal_type() == 'PositiveIntegerField', (
        'Creature.defense no es del tipo esperado'
    )
    assert f.default == 0, 'Creature.defense no tiene el valor por defecto esperado'
    assert not f.blank, 'Creature.defense no debe admitir valores en blanco'

    # speed
    assert (f := Creature._meta.get_field('speed')), 'Creature.speed no se ha definido'
    assert f.get_internal_type() == 'PositiveIntegerField', 'Creature.speed no es del tipo esperado'
    assert f.default == 0, 'Creature.speed no tiene el valor por defecto esperado'
    assert not f.blank, 'Creature.speed no debe admitir valores en blanco'

    # generation
    assert (f := Creature._meta.get_field('generation')), 'Creature.generation no se ha definido'
    assert f.get_internal_type() == 'PositiveSmallIntegerField', (
        'Creature.generation no es del tipo esperado'
    )
    assert f.default == 1, 'Creature.generation no tiene el valor por defecto esperado'
    assert not f.blank, 'Creature.generation no debe admitir valores en blanco'
