from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditWaveForm
from .models import Wave


@login_required
def edit_wave(request, wave_pk):
    wave = get_object_or_404(Wave, pk=wave_pk)

    # Comprobar si el usuario logueado es el autor (si no, devuelve un error 403)
    if wave.user != request.user:
        raise PermissionDenied('No eres el autor de este wave.')

    if request.method == 'POST':
        form = EditWaveForm(request.POST, instance=wave)
        if form.is_valid():
            form.save()

            messages.success(request, 'Wave updated successfully.')
            return redirect(wave)  # Redirige al echo correspondiente
    else:
        form = EditWaveForm(instance=wave)

    context = {
        'form': form,
        'wave': wave,
    }
    return render(request, 'waves/wave/edit.html', context)


@login_required
def delete_wave(request, wave_pk):
    wave = get_object_or_404(Wave, pk=wave_pk)

    # Comprobar si el usuario logueado es el autor (si no, devuelve un error 403)
    if wave.user != request.user:
        raise PermissionDenied('No eres el autor de este wave.')

    echo = wave.echo
    if request.method == 'POST':
        wave.delete()
        messages.success(request, 'Wave deleted successfully.')
        return redirect(echo)  # Redirige al echo correspondiente
    return redirect(echo)
