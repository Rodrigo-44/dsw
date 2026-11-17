from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from echos.models import Echo

from .forms import ProfileForm
from .models import Profile


@login_required
def user_list(request):
    profiles = Profile.objects.all().order_by('user__username')

    return render(
        request,
        'users/profile/list.html',
        {'profiles': profiles},
    )


@login_required
def user_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    all_echos_count = Echo.objects.filter(user=profile.user).count()
    echos = Echo.objects.filter(user=profile.user).order_by('-created_at')[:5]

    return render(
        request,
        'users/profile/detail.html',
        {
            'profile': profile,
            'echos': echos,
            'all_echos_count': all_echos_count,
        },
    )


@login_required
def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.user.pk != profile.user.pk:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('users:me')
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        'users/profile/edit.html',
        {'form': form},
    )


@login_required
def my_user_detail(request):
    return redirect(
        'users:user-detail',
        username=request.user.username,
    )


@login_required
def user_echos(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    echos = Echo.objects.filter(user=profile.user).order_by('-created_at')

    return render(
        request,
        'users/user_echos.html',
        {
            'profile': profile,
            'echos': echos,
        },
    )
