import pytest

from factories import AppointmentFactory, SlotFactory, UserFactory

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

APPOINTMENT_LIST_URL = '/appointments/'
APPOINTMENT_DETAIL_URL = '/appointments/{appointment_pk}/'
APPOINTMENT_ADD_URL = '/appointments/add/'

ADMIN_CHANGE_URL = '/admin/{app_label}/{model_name}/{object_pk}/'

# ==============================================================================
# Helpers
# ==============================================================================


def str_slot(slot):
    return f'{slot.start_at.strftime("%H:%M")} - {slot.end_at.strftime("%H:%M")}'


def str_appointment(appointment):
    return f'{appointment.date} ({str_slot(appointment.slot)})'


def str(item):
    match item.__class__.__name__:
        case 'Slot':
            return str_slot(item)
        case 'Appointment':
            return str_appointment(item)
        case _:
            return str(item)


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def another_user():
    return UserFactory()


@pytest.fixture
def slot():
    return SlotFactory()


@pytest.fixture
def another_slot():
    return SlotFactory()


@pytest.fixture
def appointment():
    return AppointmentFactory()
