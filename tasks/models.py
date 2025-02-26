from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth.models import User


class Task(models.Model):
    CATEGORY_CHOICES = [
        ("estadistica_informacion", "Estadística e Información"),
        ("planeacion_estrategia", "Planeación y Estrategia"),
        ("procesos_r", "Procesos /R"),
        ("alianzas", "Alianzas"),
    ]

    STATUS_CHOICES = [
        ("in_progress", "En Proceso"),
        ("due_soon", "Próximo a Vencer"),
        ("overdue", "Venció"),
        ("completed", "Finalizado"),
    ]

    MODEL_CHOICES = [
        ("alianzas", "Alianzas Año Presente"),
        ("planeacion", "Planeación Estrategia Año Presente"),
        ("estadistica", "Estadística Información Año Presente"),
        ("procesos", "Procesos R Año Presente"),
        ("none", "Ninguno"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()  # Fecha límite de la tarea
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="in_progress"
    )
    created_at = models.DateTimeField()
    alianza = models.CharField(max_length=200, blank=True, null=True)
    dependencies = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="dependent_tasks"
    )

    related_model_type = models.CharField(
        max_length=20,
        choices=MODEL_CHOICES,
        default="none",
        verbose_name="Tipo de modelo relacionado",
    )

    # Relación con usuarios
    assigned_users = models.ManyToManyField(User, blank=True, related_name="tasks")

    # Campos para las relaciones con los modelos específicos
    alianzas_object = models.ForeignKey(
        "manager.AlianzasAñoPresente",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_tasks",
    )
    planeacion_object = models.ForeignKey(
        "manager.PlaniacionEstrategiaAñoPresente",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_tasks",
    )
    estadistica_object = models.ForeignKey(
        "manager.EstadisticaInformacionAñoPresente",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_tasks",
    )
    procesos_object = models.ForeignKey(
        "manager.ProcesosRAñoPresente",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_tasks",
    )

    def __str__(self):
        return self.title

    def is_due(self):
        """Verifica si la tarea ha vencido y genera una alerta si es el caso"""
        due_date = (
            timezone.make_aware(self.due_date)
            if self.due_date.tzinfo is None
            else self.due_date
        )
        now = timezone.now()

        if due_date <= now:
            return f"ALERTA: La tarea '{self.title}' ha vencido."
        return "La tarea está dentro del plazo."

    def is_overlapping(self, other_task):
        """Verifica si la tarea se solapa con otra tarea en la misma fecha y genera una alerta"""
        if self.due_date.date() == other_task.due_date.date():
            return f"ALERTA: La tarea '{self.title}' se solapa con la tarea '{other_task.title}' en la misma fecha."
        return "No hay solapamiento con otras tareas."


@receiver(pre_save, sender=Task)
def update_task_status(sender, instance, **kwargs):
    if instance.status != "completed":
        now = timezone.now()
        due_date = (
            timezone.make_aware(instance.due_date)
            if not instance.due_date.tzinfo
            else instance.due_date
        )

        if due_date < now - timezone.timedelta(days=1):
            instance.status = "overdue"
        elif due_date - timezone.timedelta(days=5) <= now <= due_date:
            instance.status = "due_soon"
        else:
            instance.status = "in_progress"


@receiver(post_migrate)
def update_existing_tasks(sender, **kwargs):
    if sender.name == "tasks":  # Asegúrate de que solo se ejecute para tu app de tareas
        Task = apps.get_model("tasks", "Task")
        tasks = Task.objects.all()
        now = timezone.now()

        for task in tasks:
            if task.status != "completed":
                due_date = (
                    timezone.make_aware(task.due_date)
                    if not task.due_date.tzinfo
                    else task.due_date
                )

                if due_date < now - timezone.timedelta(days=1):
                    task.status = "overdue"
                elif due_date - timezone.timedelta(days=5) <= now <= due_date:
                    task.status = "due_soon"
                else:
                    task.status = "in_progress"

                task.save()


class WeeklyTask(models.Model):
    CATEGORY_CHOICES = [
        ("estadistica_informacion", "Estadística e Información"),
        ("planeacion_estrategia", "Planeación y Estrategia"),
        ("procesos_r", "Procesos /R"),
        ("alianzas", "Alianzas"),
    ]

    STATUS_CHOICES = [
        ("in_progress", "En Proceso"),
        ("due_soon", "Próximo a Vencer"),
        ("overdue", "Venció"),
        ("completed", "Finalizado"),
    ]

    DAY_CHOICES = [
        ("monday", "Lunes"),
        ("tuesday", "Martes"),
        ("wednesday", "Miércoles"),
        ("thursday", "Jueves"),
        ("friday", "Viernes"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="in_progress"
    )
    evaluation_day = models.CharField(max_length=10, choices=DAY_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.get_evaluation_day_display()}"

    def update_status(self):
        """Actualiza el estado de la tarea según el día actual"""
        if self.status == "completed":
            # Si es lunes y está completada, volver a "in_progress"
            current_weekday = timezone.now().strftime("%A").lower()
            if current_weekday == "monday":
                self.status = "in_progress"
                self.save()
            return

        # Obtener el día actual y el día de evaluación
        current_date = timezone.now().date()
        current_weekday = current_date.strftime("%A").lower()

        # Encontrar la fecha del día de evaluación esta semana
        weekday_mapping = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
        }

        days_until_evaluation = (
            weekday_mapping[self.evaluation_day] - weekday_mapping[current_weekday]
        ) % 7

        evaluation_date = current_date + timedelta(days=days_until_evaluation)

        # Actualizar el estado según las reglas
        if current_weekday in ["monday", "tuesday", "wednesday"]:
            self.status = "in_progress"
        elif current_weekday in ["thursday", "friday"]:
            self.status = "due_soon"
        elif current_date > evaluation_date:
            self.status = "overdue"

        self.save()

    @classmethod
    def update_all_tasks(cls):
        """Actualiza el estado de todas las tareas"""
        for task in cls.objects.all():
            task.update_status()


# Ejemplo de cómo programar la actualización automática usando Django Celery
from celery import shared_task


@shared_task
def update_weekly_tasks():
    WeeklyTask.update_all_tasks()
