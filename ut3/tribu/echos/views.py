from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from waves.forms import AddWaveForm

from .forms import AddEchoForm, EditEchoForm
from .models import Echo


@login_required
def echo_list(request):
    echos = Echo.objects.all().order_by('-created_at')
    total_echos = echos.count()
    return render(
        request,
        'echos/echo/list.html',
        {'echo': echos, 'total_echos': total_echos},
    )


@login_required
def add_echo(request):
    if request.method == 'POST':
        form = AddEchoForm(request.POST)

        if form.is_valid():
            echo = form.save(commit=False)
            echo.user = request.user
            echo.save()

            messages.success(request, 'Echo added successfully')
            return redirect(echo)
    else:
        form = AddEchoForm()

    return render(request, 'echos/echo/add.html', {'form': form})


@login_required
def edit_echo(request, echo):

    # Comprobar si el usuario logueado es el autor (si no, devuelve un error 403)
    if echo.user != request.user:
        raise PermissionDenied('No eres el autor de este echo.')

    if request.method == 'POST':
        form = EditEchoForm(request.POST, instance=echo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Echo updated successfully.')
            return redirect(echo)  # Método get_absolute_url()
    else:
        form = EditEchoForm(instance=echo)

    context = {
        'form': form,
        'echo': echo,
    }
    return render(request, 'echos/echo/edit.html', context)


@login_required
def delete_echo(request, echo):

    # Comprobar si el usuario logueado es el autor (si no, devuelve un error 403)
    if echo.user != request.user:
        raise PermissionDenied('No eres el autor de este echo.')
    echo.delete()
    messages.success(request, 'Echo deleted successfully.')
    return redirect('echos:echo-list')


@login_required
def echo_detail(request, echo):
    waves = echo.waves.all()[:5]
    return render(
        request,
        'echos/echo/detail.html',
        {
            'echo': echo,
            'waves': waves,
            'request': request,
        },
    )


@login_required
def echo_waves(request, echo):
    waves = echo.waves.all()
    return render(
        request,
        'echos/echo/waves/wave/all-waves.html',
        {
            'echo': echo,
            'waves': waves,
            'request': request,
        },
    )


@login_required
def add_wave(request, echo):
    if request.method == 'POST':
        form = AddWaveForm(request.POST)

        if form.is_valid():
            wave = form.save(commit=False)
            wave.user = request.user
            wave.echo = echo
            wave.save()

            messages.success(request, 'Wave added successfully')
            return redirect(echo)
    else:
        form = AddWaveForm()

    return render(
        request,
        'echos/echo/waves/wave/add.html',
        {'form': form, 'echo': echo},
    )
