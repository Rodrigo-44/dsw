import pytest

from factories import TaskFactory
from tasks.models import Task

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


TASK_LIST_URL = '/tasks/'
TASK_LIST_COMPLETED_URL = '/tasks/completed/'
TASK_LIST_PENDING_URL = '/tasks/pending/'
TASK_DETAIL_URL = '/tasks/{task_slug}/'
TASK_TOGGLE_URL = '/tasks/{task_slug}/toggle/'
TASK_EDIT_URL = '/tasks/{task_slug}/edit/'
TASK_DELETE_URL = '/tasks/{task_slug}/delete/'
TASK_ADD_URL = '/tasks/add/'

# ==============================================================================
# Helpers
# ==============================================================================


def get_url_and_tasks(completed: bool | None):
    match completed:
        case None:
            url = TASK_LIST_URL
            included_tasks = Task.objects.all()
            excluded_tasks = []
        case True:
            url = TASK_LIST_COMPLETED_URL
            included_tasks = Task.objects.filter(completed=True)
            excluded_tasks = Task.objects.filter(completed=False)
        case False:
            url = TASK_LIST_PENDING_URL
            included_tasks = Task.objects.filter(completed=False)
            excluded_tasks = Task.objects.filter(completed=True)
    return url, included_tasks, excluded_tasks


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def task():
    return TaskFactory()
