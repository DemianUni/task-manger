from tasks.models import Task
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    ResultadoAñoPasadoGenerales,
    ResultadoAñoPasadoAlianzas,
    AlianzasAñoPresente,
    PlaniacionEstrategiaAñoPresente,
    EstadisticaInformacionAñoPresente,
    ProcesosRAñoPresente,
)
from .forms import (
    ResultadoAPGForm,
    ResultadoAPAForm,
    AlianzasAPForm,
    PlaniacionEstrategiaAPForm,
    EstadisticaInformacionAPForm,
    ProcesosRAPForm,
)
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = AuthenticationForm()

    return render(request, "menu.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(request.META.get("HTTP_REFERER", "/"))


def get_years():
    # Obtener el año actual
    current_year = datetime.now().year
    # Calcular el año pasado
    last_year = current_year - 1
    return {"last_year": last_year, "current_year": current_year}


def menu(request):
    years = get_years()
    return render(request, "menu.html", years)


def resultados_año_pasado(request):
    generales = ResultadoAñoPasadoGenerales.objects.all()
    alianzas = ResultadoAñoPasadoAlianzas.objects.all()

    context = {
        "last_year": datetime.now().year - 1,
        "generales": generales,
        "alianzas": alianzas,
        "form_generales": ResultadoAPGForm(),
        "form_alianzas": ResultadoAPAForm(),
    }
    return render(request, "resultados_año_pasado.html", context)


def agregar_general(request):
    if request.method == "POST":
        form = ResultadoAPGForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("resultados_año_pasado")


def agregar_alianza(request):
    if request.method == "POST":
        form = ResultadoAPAForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("resultados_año_pasado")


def editar_general(request, pk):
    general = get_object_or_404(ResultadoAñoPasadoGenerales, pk=pk)
    if request.method == "POST":
        form = ResultadoAPGForm(request.POST, instance=general)
        if form.is_valid():
            form.save()
    return redirect("resultados_año_pasado")


def eliminar_general(request, pk):
    if request.method == "POST":
        general = get_object_or_404(ResultadoAñoPasadoGenerales, pk=pk)
        general.delete()
    return redirect("resultados_año_pasado")


def editar_alianza(request, pk):
    alianza = get_object_or_404(ResultadoAñoPasadoAlianzas, pk=pk)
    if request.method == "POST":
        form = ResultadoAPAForm(request.POST, instance=alianza)
        if form.is_valid():
            form.save()
    return redirect("resultados_año_pasado")


def eliminar_alianza(request, pk):
    if request.method == "POST":
        alianza = get_object_or_404(ResultadoAñoPasadoAlianzas, pk=pk)
        alianza.delete()
    return redirect("resultados_año_pasado")


# Vista para la página de Proyectos 2025
def proyectos_año_presente(request):
    years = get_years()
    return render(request, "proyectos_año_presente.html", years)


# Estadistica Informacion
def estadistica_informacion(request):
    years = get_years()
    estadistica_informacion = EstadisticaInformacionAñoPresente.objects.all()
    tasks_estadistica_informacion = Task.objects.filter(
        category="estadistica_informacion"
    )
    return render(
        request,
        "estadistica_informacion.html",
        {
            "years": years,
            "tasks_estadistica_informacion": tasks_estadistica_informacion,
            "estadistica_informacion": estadistica_informacion,
        },
    )


# Funciones
def agregar_estadistica_informacion(request):
    if request.method == "POST":
        form = EstadisticaInformacionAPForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("estadistica_informacion")


def editar_estadistica_informacion(request, pk):
    estadistica_informacion = get_object_or_404(
        EstadisticaInformacionAñoPresente, pk=pk
    )
    if request.method == "POST":
        form = EstadisticaInformacionAPForm(
            request.POST, instance=estadistica_informacion
        )
        if form.is_valid():
            form.save()
    return redirect("estadistica_informacion")


def eliminar_estadistica_informacion(request, pk):
    if request.method == "POST":
        estadistica_informacion = get_object_or_404(
            EstadisticaInformacionAñoPresente, pk=pk
        )
        estadistica_informacion.delete()
    return redirect("estadistica_informacion")


# Planeacion Estrategia
def planeacion_estrategia(request):
    years = get_years()
    tasks_planeacion_estrategia = Task.objects.filter(category="planeacion_estrategia")
    planeacion_estrategia = PlaniacionEstrategiaAñoPresente.objects.all()
    return render(
        request,
        "planeacion_estrategia.html",
        {
            "years": years,
            "tasks_planeacion_estrategia": tasks_planeacion_estrategia,
            "planeacion_estrategia": planeacion_estrategia,
        },
    )


# Funciones
def agregar_planeacion_estrategia(request):
    if request.method == "POST":
        form = PlaniacionEstrategiaAPForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("planeacion_estrategia")


def editar_planeacion_estrategia(request, pk):
    planeacion_estrategia = get_object_or_404(PlaniacionEstrategiaAñoPresente, pk=pk)
    if request.method == "POST":
        form = PlaniacionEstrategiaAPForm(request.POST, instance=planeacion_estrategia)
        if form.is_valid():
            form.save()
    return redirect("planeacion_estrategia")


def eliminar_planeacion_estrategia(request, pk):
    if request.method == "POST":
        planeacion_estrategia = get_object_or_404(
            PlaniacionEstrategiaAñoPresente, pk=pk
        )
        planeacion_estrategia.delete()
    return redirect("planeacion_estrategia")


# Procesos /R
def procesos_r(request):
    years = get_years()
    procesos_r = ProcesosRAñoPresente.objects.all()
    tasks_procesosR = Task.objects.filter(category="procesos_r")
    return render(
        request,
        "procesos_r.html",
        {"years": years, "procesos_r": procesos_r, "tasks_procesosR": tasks_procesosR},
    )


# Funciones
def agregar_procesos_r(request):
    if request.method == "POST":
        form = ProcesosRAPForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("procesos_r")


def editar_procesos_r(request, pk):
    procesos_r = get_object_or_404(ProcesosRAñoPresente, pk=pk)
    if request.method == "POST":
        form = ProcesosRAPForm(request.POST, instance=procesos_r)
        if form.is_valid():
            form.save()
    return redirect("procesos_r")


def eliminar_procesos_r(request, pk):
    if request.method == "POST":
        procesos_r = get_object_or_404(ProcesosRAñoPresente, pk=pk)
        procesos_r.delete()
    return redirect("procesos_r")


# Alianzas
def alianzas(request):
    years = get_years()
    tasks_alianzas = Task.objects.filter(category="alianzas")
    alianzas = AlianzasAñoPresente.objects.all()

    return render(
        request,
        "alianzas.html",
        {"years": years, "tasks_alianzas": tasks_alianzas, "alianzas": alianzas},
    )


# Funciones
def agregar_alianza_presente(request):
    if request.method == "POST":
        form = AlianzasAPForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("alianzas")


def editar_alianza_presente(request, pk):
    alianza = get_object_or_404(AlianzasAñoPresente, pk=pk)
    if request.method == "POST":
        form = AlianzasAPForm(request.POST, instance=alianza)
        if form.is_valid():
            form.save()
    return redirect("alianzas")


def eliminar_alianza_presente(request, pk):
    if request.method == "POST":
        alianza = get_object_or_404(AlianzasAñoPresente, pk=pk)
        alianza.delete()
    return redirect("alianzas")
