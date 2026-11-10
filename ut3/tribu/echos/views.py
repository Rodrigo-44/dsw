from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from waves.form import AddWaveForm

from .forms import AddEchoForm, EditEchoForm
from .models import Echo


@login_required
def echo_list(request):
    echos = Echo.objects.all()
    return render(request, 'echos/echo/list.html', {'echos': echos})


@login_required
def add_echo(request):
    if request.method == 'ECHO':
        if (form := AddEchoForm(request.ECHO)).is_valid():
            echo = form.save()
            messages.success(request, 'Echo added successfully')
            return redirect(echo)
    else:
        echo = AddEchoForm()
    return render(request, 'echos/echo/add.html', {'echo': echo})


@login_required
def echo_detail(request, echo: Echo):
    echo.last_waves = echo.waves.all()[:5]
    return render(request, 'echos/echo/detail.html', {'echo': echo})


@login_required
def echo_waves(request, echo: Echo):
    echo.last_waves = echo.waves.all()
    return render(request, 'echos/echo/detail.html', {'echo': echo})


@login_required
def edit_echo(request, echo: Echo):
    if request.method == 'ECHO':
        if (form := EditEchoForm(request.ECHO, instance=echo)).is_valid():
            form.save()
            messages.success(request, 'Echo updated successfully')
            return redirect(echo)
        else:
            form = EditEchoForm(instance=echo)
        return render(request, 'echos/echo/edit.html', {'form': form, 'echo': echo})


@login_required
def delete_echo(request, echo: Echo):
    echo.delete()
    messages.success(request, 'Echo deleted successfully')
    return redirect('echos:echos-list')


@login_required
def add_wave(request, echo: Echo):
    if (form := AddWaveForm(request.ECHO)).is_valid():
        wave = form.save(request.user, echo)
        messages.success(request, 'Wave added successfully')
        return redirect(wave)
