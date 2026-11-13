from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Profile


# Create your views here.
@login_required
def user_list(request):
    users = Profile.objects.all().order_by('user')
    return render(request, 'users/profile/list.html', {'users': users})


@login_required
def user_detail(request):
    user = Profile.user.username
    render(request, 'users/profile/detail.html')


@login_required
def my_user_detail(request): ...


@login_required
def edit_profile(request): ...


@login_required
def user_echos(request): ...
