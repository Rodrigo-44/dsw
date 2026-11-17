from django.urls import path

from . import views

app_name = ''


urlpatterns = [
    path('', views.welcome, name='post-list'),
]
