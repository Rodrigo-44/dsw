from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Appointment


@login_required
def appoinment_detail(request, appointment):
    appointment = get_object_or_404(Appointment, pk=appointment.pk)
    return render(request, 'appointments/appointment/detail.html', {'appoinment': appointment})


@login_required
def add_post(request):
    pass
