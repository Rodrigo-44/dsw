from django.urls import path, register_converter

from . import converters, views

app_name = 'echos'
register_converter(converters.EchoConverter, 'echo')

urlpatterns = [
    path('', views.echo_list, name='echos-list'),
    # path('add/', views.add_post, name='add-post'),
    # path(
    #    '<post:post>/', views.post_detail, name='post-detail'
    # ),  # el pirmero es el conversor el segundo es el parametro de la vista
    # path('<post:post>/edit/', views.edit_post, name='edit-post'),
    # path('<post:post>/delete/', views.delete_post, name='delete-post'),
    # path('<post:post>/comments/add', views.add_comment, name='add-comments'),
]
