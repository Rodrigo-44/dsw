import re

import pytest

from tests import conftest


@pytest.mark.django_db
def test_template_inheritance(client):
    response = client.get(conftest.TASK_LIST_URL)
    assert 'base.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_template_includes(client):
    response = client.get(conftest.TASK_LIST_URL)
    assert re.search('(includes/)?header.html', ''.join([t.name for t in response.templates]))


@pytest.mark.django_db
def test_template_contains_css_links(client):
    response = client.get(conftest.TASK_LIST_URL)
    response_text = response.content.decode()
    assert re.search(
        r'<link[^>]+href="[^"]+(main|custom|styles?)\.css"', response_text, re.S | re.M
    )
