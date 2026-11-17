from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditWaveForm
from .models import Wave


@login_required
def edit_wave(request, wave_pk):
    wave = get_object_or_404(Wave, pk=wave_pk)

    if wave.user != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        form = EditWaveForm(request.POST, instance=wave)

        if form.is_valid():
            form.save()
            messages.success(request, 'Wave updated successfully')
            return redirect(wave)
    else:
        form = EditWaveForm(instance=wave)

    return render(
        request,
        'waves/wave/edit.html',
        {
            'form': form,
            'wave': wave,
        },
    )


@login_required
def delete_wave(request, wave_pk):
    wave = get_object_or_404(Wave, pk=wave_pk)

    if wave.user != request.user:
        raise PermissionDenied()

    echo = wave.echo
    wave.delete()

    messages.success(request, 'Wave deleted successfully')
    return redirect(echo)
