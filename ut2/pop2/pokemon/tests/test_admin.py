import pytest
from django.contrib import admin

from creatures.models import Creature


@pytest.mark.parametrize(
    'model',
    [Creature],
)
@pytest.mark.django_db
def test_models_are_registered_in_admin(model):
    assert model in admin.site._registry, (
        f'El modelo "{model.__name__}" no está registrado en el admin'
    )
