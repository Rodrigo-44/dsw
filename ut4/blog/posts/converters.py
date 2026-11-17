from django.shortcuts import get_object_or_404

from .models import Post


class PostConverter:
    regex = r'[\w-]+'

    def to_python(self, post_slug: str) -> Post:
        return get_object_or_404(Post, slug=post_slug)

    def to_url(self, post: Post) -> str:
        return post.slug
