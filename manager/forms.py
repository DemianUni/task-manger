# forms.py
from django import forms
from .models import (
    ResultadoAñoPasadoGenerales,
    ResultadoAñoPasadoAlianzas,
    AlianzasAñoPresente,
    PlaniacionEstrategiaAñoPresente,
    EstadisticaInformacionAñoPresente,
    ProcesosRAñoPresente,
)


# Resutados Año Pasado
class ResultadoAPGForm(forms.ModelForm):
    class Meta:
        model = ResultadoAñoPasadoGenerales
        fields = ["title", "description"]


class ResultadoAPAForm(forms.ModelForm):
    class Meta:
        model = ResultadoAñoPasadoAlianzas
        fields = ["title", "description"]


# Proyectos Año Presente
class AlianzasAPForm(forms.ModelForm):
    class Meta:
        model = AlianzasAñoPresente
        fields = ["title", "description"]


class PlaniacionEstrategiaAPForm(forms.ModelForm):
    class Meta:
        model = PlaniacionEstrategiaAñoPresente
        fields = ["title", "description"]


class EstadisticaInformacionAPForm(forms.ModelForm):
    class Meta:
        model = EstadisticaInformacionAñoPresente
        fields = ["title", "description"]


class ProcesosRAPForm(forms.ModelForm):
    class Meta:
        model = ProcesosRAñoPresente
        fields = ["title", "description"]
