import re

import pytest

from echos.models import Echo
from waves.models import Wave


def test_template_inheritance(client):
    response = client.get('/')
    assert 'base.html' in [t.name for t in response.templates]


def test_template_includes(client):
    response = client.get('/')
    assert re.search('(includes/)?header.html', ''.join([t.name for t in response.templates]))


def test_template_contains_css_links(client):
    response = client.get('/')
    response_text = response.content.decode()
    assert re.search(
        r'<link[^>]+href="[^"]+(main|custom|styles?)\.css"', response_text, re.S | re.M
    )


def test_message_middleware_is_enabled(settings):
    assert 'django.contrib.messages.middleware.MessageMiddleware' in settings.MIDDLEWARE


@pytest.mark.parametrize(
    'model',
    [Echo, Wave],
)
@pytest.mark.django_db
def test_model_contains_get_absolute_url_method(model):
    assert hasattr(model, 'get_absolute_url')
    assert callable(getattr(model, 'get_absolute_url'))
