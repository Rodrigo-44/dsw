import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

from echos.models import Echo
from users.models import Profile
from waves.models import Wave

User = get_user_model()

# ==============================================================================
# Required Apps
# ==============================================================================


@pytest.mark.django_db
def test_required_apps_are_installed():
    REQUIRED_APPS = ('shared', 'accounts', 'echos', 'waves', 'users')

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
# Profile Model
# ==============================================================================


@pytest.mark.score(2)
@pytest.mark.django_db
def test_profile_model_is_correctly_configured():
    # user
    assert (f := Profile._meta.get_field('user')), 'Profile.user no se ha definido'
    assert f.get_internal_type() == 'OneToOneField', 'Profile.user no tiene el tipo esperado'
    assert f.remote_field.model == User, 'Profile.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Profile.user no tiene el método de borrado esperado'
    )
    assert not f.blank, 'Profile.user no debe admitir valores en blanco'

    # avatar
    assert (f := Profile._meta.get_field('avatar')), 'Profile.avatar no se ha definido'
    assert f.get_internal_type() in ['FileField', 'ImageField'], (
        'Profile.avatar no tiene el tipo esperado'
    )
    assert f.upload_to == 'avatars', 'Profile.avatar no tiene la ruta de subida esperada'
    assert f.default == 'avatars/noavatar.png', (
        'Profile.avatar no tiene el valor por defecto esperado'
    )
    assert not f.blank, 'Profile.avatar no debe admitir valores en blanco'

    # bio
    assert (f := Profile._meta.get_field('bio')), 'Profile.bio no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Profile.bio no tiene el tipo esperado'
    assert f.blank, 'Profile.bio no admite valores en blanco'


# ==============================================================================
# Echo Model
# ==============================================================================


@pytest.mark.score(2)
@pytest.mark.django_db
def test_echo_model_is_correctly_configured():
    # content
    assert (f := Echo._meta.get_field('content')), 'Echo.content no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Echo.content no tiene el tipo esperado'
    assert not f.blank, 'Echo.content no debe admitir valores en blanco'

    # created_at
    assert (f := Echo._meta.get_field('created_at')), 'Echo.created_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Echo.created_at no tiene el tipo esperado'
    assert f.auto_now_add, 'Echo.created_at no está configurado con auto_now_add'

    # updated_at
    assert (f := Echo._meta.get_field('updated_at')), 'Echo.updated_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Echo.updated_at no tiene el tipo esperado'
    assert f.auto_now, 'Echo.updated_at no está configurado con auto_now'

    # user
    assert (f := Echo._meta.get_field('user')), 'Echo.user no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Echo.user no tiene el tipo esperado'
    assert f.remote_field.model == User, 'Echo.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Echo.user no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'echos', 'Echo.user no tiene el related_name esperado'
    assert not f.blank, 'Echo.user no debe admitir valores en blanco'


# ==============================================================================
# Wave Model
# ==============================================================================


@pytest.mark.score(2)
@pytest.mark.django_db
def test_wave_model_is_correctly_configured():
    # content
    assert (f := Wave._meta.get_field('content')), 'Wave.content no se ha definido'
    assert f.get_internal_type() == 'TextField', 'Wave.content no tiene el tipo esperado'
    assert not f.blank, 'Wave.content no debe admitir valores en blanco'

    # created_at
    assert (f := Wave._meta.get_field('created_at')), 'Wave.created_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Wave.created_at no tiene el tipo esperado'
    assert f.auto_now_add, 'Wave.created_at no está configurado con auto_now_add'

    # updated_at
    assert (f := Wave._meta.get_field('updated_at')), 'Wave.updated_at no se ha definido'
    assert f.get_internal_type() == 'DateTimeField', 'Wave.updated_at no tiene el tipo esperado'
    assert f.auto_now, 'Wave.updated_at no está configurado con auto_now'

    # user
    assert (f := Wave._meta.get_field('user')), 'Wave.user no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Wave.user no tiene el tipo esperado'
    assert f.remote_field.model == User, 'Wave.user no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Wave.user no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'waves', 'Wave.user no tiene el related_name esperado'
    assert not f.blank, 'Wave.user no debe admitir valores en blanco'

    # echo
    assert (f := Wave._meta.get_field('echo')), 'Wave.echo no se ha definido'
    assert f.get_internal_type() == 'ForeignKey', 'Wave.echo no es del tipo esperado'
    assert f.remote_field.model == Echo, 'Wave.echo no referencia al modelo esperado'
    assert f.remote_field.on_delete.__name__ == 'CASCADE', (
        'Wave.echo no tiene el método de borrado esperado'
    )
    assert f.remote_field.related_name == 'waves', 'Wave.echo no tiene el related_name esperado'
    assert not f.blank, 'Wave.echo no debe admitir valores en blanco'
