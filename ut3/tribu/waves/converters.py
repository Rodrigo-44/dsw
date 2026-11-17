from django.shortcuts import get_object_or_404

from .models import Wave


class WaveConverter:
    regex = r'\d+'

    def to_python(self, wave_pk: str) -> Wave:
        return get_object_or_404(Wave, pk=int(wave_pk))

    def to_url(self, wave: Wave) -> str:
        return str(wave.pk if hasattr(wave, 'pk') else wave)
