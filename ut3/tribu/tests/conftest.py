import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from factories import EchoFactory, UserFactory, WaveFactory

# ==============================================================================
# SCORE
# ==============================================================================


DEFAULT_SCORE = 1
TOTAL_SCORE = 0
MAX_SCORE = 0


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, *args, **kwargs):
    global TOTAL_SCORE, MAX_SCORE

    outcome = yield
    rep = outcome.get_result()

    # Solo evaluamos el resultado final del test
    if rep.when != 'call':
        return

    if marker := item.get_closest_marker('score'):
        score = marker.args[0]
    else:
        score = DEFAULT_SCORE

    # El score máximo siempre cuenta
    MAX_SCORE += score

    # El score obtenido solo si pasa
    if rep.passed:
        TOTAL_SCORE += score


def pytest_sessionfinish(*args, **kwargs):
    SEP_WIDTH = 30

    print('\n\n' + '=' * SEP_WIDTH)
    print('🏁 RESULTADO FINAL')
    print(f'✅ Score obtenido: {TOTAL_SCORE}')
    print(f'📊 Score máximo:   {MAX_SCORE}')

    if MAX_SCORE > 0:
        percentage = (TOTAL_SCORE / MAX_SCORE) * 100
        percentage_r = round(TOTAL_SCORE / MAX_SCORE, 1) * 100
        print(f'📈 Porcentaje:     {percentage:.2f}%')
        print(f'📝 Porcentaje (R): {percentage_r:.0f}%')

    print('=' * SEP_WIDTH)


# ==============================================================================
# URL Patterns
# ==============================================================================

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
SIGNUP_URL = '/signup/'

ECHO_LIST_URL = '/echos/'
ECHO_DETAIL_URL = '/echos/{echo_pk}/'
ECHO_ADD_URL = '/echos/add/'
ECHO_WAVES_URL = '/echos/{echo_pk}/waves/'
ECHO_EDIT_URL = '/echos/{echo_pk}/edit/'
ECHO_DELETE_URL = '/echos/{echo_pk}/delete/'

WAVE_ADD_URL = '/echos/{echo_pk}/waves/add/'
WAVE_EDIT_URL = '/waves/{wave_pk}/edit/'
WAVE_DELETE_URL = '/waves/{wave_pk}/delete/'

USER_LIST_URL = '/users/'
USER_DETAIL_URL = '/users/{username}/'
USER_ECHOS_URL = '/users/{username}/echos/'

PROFILE_ME_URL = '/users/@me/'
PROFILE_EDIT_URL = '/users/{username}/edit/'

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_without_profile():
    return UserFactory(profile=None)


@pytest.fixture
def another_user():
    return UserFactory()


@pytest.fixture
def another_user_without_profile():
    return UserFactory(profile=None)


@pytest.fixture
def echo(user):
    return EchoFactory(user=user)


@pytest.fixture
def wave(user, echo):
    return WaveFactory(user=user, echo=echo)


@pytest.fixture
def image():
    img = Image.new('RGBA', size=(200, 200), color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return SimpleUploadedFile(
        name='test_image.png',
        content=buffer.getvalue(),
        content_type='image/png',
    )


@pytest.fixture(autouse=True)
def media_tmpdir(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / 'media'
