from django import forms

from .models import Task


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description')
        labels = {
            'name': 'Nombre de la tarea',
            'description': 'Descripción de la tarea',
        }


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description')
        labels = {
            'name': 'Nombre de la tarea',
            'description': 'Descripción de la tarea',
        }
