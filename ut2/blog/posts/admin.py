from django.contrib import admin
from django.utils.text import slugify

from .models import Post


@admin.action(description='Regenerate slug (from title) for selected posts')
def regenerate_slug(modeladmin, request, queryset):
    for post in queryset:
        post.slug = slugify(post.title)
        post.save()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published')
    search_fields = ('title', 'content')
    list_filter = ('published',)
    actions = [regenerate_slug]
    # prepopulated_fields = {'slug': ('title',)}
