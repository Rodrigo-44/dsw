from django.contrib import admin

from .models import Profile


@admin.register(Profile)  # Siempre debe existir contenido dentro del parentesis
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation', 'phone')
