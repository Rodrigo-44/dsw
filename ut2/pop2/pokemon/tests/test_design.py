import pytest

from tests import conftest


@pytest.mark.django_db
def test_template_inheritance(client):
    response = client.get(conftest.CREATURE_LIST_URL)
    assert 'base.html' in [t.name for t in response.templates]
