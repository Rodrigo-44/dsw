from django.shortcuts import get_object_or_404

from .models import Profile


class ProfileConverter:
    regex = r'[\w.@+-]+'

    def to_python(self, username: str) -> Profile:
        return get_object_or_404(Profile, user__username=username)

    def to_url(self, profile: Profile) -> str:
        return str(profile.user.username if hasattr(profile, 'user') else profile)
