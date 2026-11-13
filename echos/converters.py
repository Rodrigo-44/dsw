from turtle import st
from django.shortcuts import get_object_or_404

from .models import Echo


class EchoConverter:
    regex = r'\d+'

    def to_python(self, echo_pk: int) -> Echo:

        return get_object_or_404(Echo, pk=int(echo_pk))

    def to_url(self, echo: Echo) -> str:
        if hasattr(echo, 'pk'):
            return str(echo.pk)
        return str(echo)
