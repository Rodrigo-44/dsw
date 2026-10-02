from django.contrib import admin

# Register your models here.
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    search_fields = ('title', 'content')
    list_filter = ('published',)
    prepopulated_fields = {'slug': ('title',)}
