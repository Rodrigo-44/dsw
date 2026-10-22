import pytest

from factories import CreatureFactory

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
# URL PATTERNS
# ==============================================================================

CREATURE_LIST_URL = '/creatures/'
CREATURE_DETAIL_URL = '/creatures/{creature_slug}/'

# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def creature():
    return CreatureFactory()
