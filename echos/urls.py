from django.urls import path, register_converter

from . import converters, views

app_name = 'echos'
register_converter(converters.EchoConverter, 'echo')

urlpatterns = [
    path('', views.echo_list, name='echo-list'),
    path('add/', views.add_echo, name='echo-add'),
    path('<echo:echo>/', views.echo_detail, name='echo-detail'),
    path('<echo:echo>/waves/', views.echo_waves, name='echo-wave'),
    path('<echo:echo>/edit/', views.edit_echo, name='echo-edit'),
    path('<echo:echo>/delete/', views.delete_echo, name='echo-delete'),
    path('<echo:echo>/waves/add/', views.add_wave, name='echo-wave-add'),
]
