from django import forms
from .models import Task, WeeklyTask
from django.contrib.auth.models import User
from manager.models import (
    AlianzasAñoPresente,
    PlaniacionEstrategiaAñoPresente,
    EstadisticaInformacionAñoPresente,
    ProcesosRAñoPresente,
)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "category",
            "status",
            "alianza",
            "dependencies",
            "created_at",
            "related_model_type",
            "alianzas_object",
            "planeacion_object",
            "estadistica_object",
            "procesos_object",
            "assigned_users",
        ]

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    created_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )
    )

    dependencies = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control select2"}),
    )

    related_model_type = forms.ChoiceField(
        choices=Task.MODEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    assigned_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Hace que los usuarios sean checkboxes
        required=False,
        label="Usuarios asignados",
    )

    alianzas_object = forms.ModelChoiceField(
        queryset=AlianzasAñoPresente.objects.all(),  # Asegúrate de importar estos modelos
        required=False,
        empty_label="Seleccionar...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    planeacion_object = forms.ModelChoiceField(
        queryset=PlaniacionEstrategiaAñoPresente.objects.all(),
        required=False,
        empty_label="Seleccionar...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    estadistica_object = forms.ModelChoiceField(
        queryset=EstadisticaInformacionAñoPresente.objects.all(),
        required=False,
        empty_label="Seleccionar...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    procesos_object = forms.ModelChoiceField(
        queryset=ProcesosRAñoPresente.objects.all(),
        required=False,
        empty_label="Seleccionar...",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class WeeklyTaskForm(forms.ModelForm):
    class Meta:
        model = WeeklyTask
        fields = ["title", "description", "category", "status", "evaluation_day"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Título de la tarea"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "evaluation_day": forms.Select(attrs={"class": "form-select"}),
        }
