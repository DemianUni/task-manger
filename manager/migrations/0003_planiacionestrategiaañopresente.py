# Generated by Django 5.1.5 on 2025-01-29 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alianzasañopresente'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaniacionEstrategiaAñoPresente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
