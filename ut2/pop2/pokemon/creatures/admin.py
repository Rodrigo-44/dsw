from django.contrib import admin

from creatures.models import Creature


# Register your models here.
@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    pass
