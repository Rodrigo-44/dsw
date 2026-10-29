from django.urls import path, register_converter

from . import converters, views

app_name = 'posts'
register_converter(converters.PostConverter, 'post')

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('add/', views.add_post, name='add-post'),
    path(
        '<post:post>/', views.post_detail, name='post-detail'
    ),  # el pirmero es el conversor el segundo es el parametro de la vista
    path('<slug:post_slug>/edit/', views.edit_post, name='edit-post'),
    path('<post:post>/delete/', views.delete_post, name='delete-post'),
    path('<slug:post_slug>/comments/add', views.add_comment, name='add-comments'),
]
