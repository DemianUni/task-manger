from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, WeeklyTask
from .forms import TaskForm, WeeklyTaskForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q


@login_required
def tasks_list(request):
    category = request.GET.get("category", "")
    search_query = request.GET.get("search", "")

    tasks = Task.objects.all()

    if category:
        tasks = tasks.filter(category=category)

    if search_query:
        tasks = tasks.filter(Q(title__unaccent__icontains=search_query))

    # Actualizar estados
    WeeklyTask.update_all_tasks()
    WeeklyTasks = WeeklyTask.objects.all()

    return render(
        request,
        "tasks_list.html",
        {"tasks": tasks, "search_query": search_query, "WeeklyTasks": WeeklyTasks},
    )


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "tasks_list"
            )  # Redirigir a la lista de tareas después de crearla
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form})


@login_required
def WeeklyTask_create(request):
    if request.method == "POST":
        form = WeeklyTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "tasks_list"
            )  # Redirigir a la lista de tareas después de crearla
    else:
        form = WeeklyTaskForm()
    return render(request, "weeklytask_form.html", {"form": form})


@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")
    else:
        form = TaskForm(instance=task)

    # Pasar la tarea actual al contexto para usarla en el template
    return render(request, "task_form.html", {"form": form, "current_task": task})


@login_required
def weeklytask_edit(request, pk):
    weeklytask = WeeklyTask.objects.get(pk=pk)
    if request.method == "POST":
        form = WeeklyTaskForm(request.POST, instance=weeklytask)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")
    else:
        form = WeeklyTaskForm(instance=weeklytask)

    # Pasar la tarea actual al contexto para usarla en el template
    return render(
        request, "weeklytask_form.html", {"form": form, "current_task": weeklytask}
    )


@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect("tasks_list")


@login_required
def weeklytask_delete(request, pk):
    task = WeeklyTask.objects.get(pk=pk)
    task.delete()
    return redirect("tasks_list")


def notifications_view(request):
    tareas = Task.objects.all()
    # Filtrar tareas cuyo status es "overdue"
    tareas_vencidas = [tarea for tarea in tareas if tarea.status == "overdue"]

    tareas_solapadas = []
    for i, tarea in enumerate(tareas):
        for otra_tarea in tareas[i + 1 :]:
            if (
                tarea.is_overlapping(otra_tarea)
                != "No hay solapamiento con otras tareas."
            ):
                tareas_solapadas.append((tarea, otra_tarea))

    tiene_notificaciones = bool(tareas_vencidas) or bool(tareas_solapadas)

    contexto = {
        "overdue_tasks": tareas_vencidas,
        "overlapping_tasks": tareas_solapadas,
        "has_notifications": tiene_notificaciones,
    }

    return render(request, "notificaciones.html", contexto)


import json
from django.core.serializers.json import DjangoJSONEncoder


def gantt_chart(request):
    tasks = Task.objects.all()

    gantt_tasks = []
    # Actualizar estados
    WeeklyTask.update_all_tasks()
    weekly_tasks = WeeklyTask.objects.all()

    for task in tasks:
        dependencies = [str(dep.id) for dep in task.dependencies.all()]
        task_data = {
            "id": task.id,
            "title": task.title,
            "start": task.created_at.strftime("%Y-%m-%d"),
            "end": task.due_date.strftime("%Y-%m-%d"),
            "category": task.category,
            "status": task.status,
            "dependencies": dependencies,
        }

        gantt_tasks.append(task_data)

    gantt_data_json = json.dumps(gantt_tasks, cls=DjangoJSONEncoder)

    return render(
        request,
        "gantt_chart.html",
        {"gantt_data": gantt_data_json, "weekly_tasks": weekly_tasks},
    )
