# Generated by Django 5.1.5 on 2025-02-21 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_procesosrañopresente'),
        ('tasks', '0008_weeklytask'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='alianzas_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_tasks', to='manager.alianzasañopresente'),
        ),
        migrations.AddField(
            model_name='task',
            name='estadistica_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_tasks', to='manager.estadisticainformacionañopresente'),
        ),
        migrations.AddField(
            model_name='task',
            name='planeacion_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_tasks', to='manager.planiacionestrategiaañopresente'),
        ),
        migrations.AddField(
            model_name='task',
            name='procesos_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_tasks', to='manager.procesosrañopresente'),
        ),
        migrations.AddField(
            model_name='task',
            name='related_model_type',
            field=models.CharField(choices=[('alianzas', 'Alianzas Año Presente'), ('planeacion', 'Planeación Estrategia Año Presente'), ('estadistica', 'Estadística Información Año Presente'), ('procesos', 'Procesos R Año Presente'), ('none', 'Ninguno')], default='none', max_length=20, verbose_name='Tipo de modelo relacionado'),
        ),
    ]
