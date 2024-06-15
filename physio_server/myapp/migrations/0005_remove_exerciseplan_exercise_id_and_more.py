# Generated by Django 5.0.6 on 2024-06-13 13:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_training_exerciseplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exerciseplan',
            name='exercise_id',
        ),
        migrations.AddField(
            model_name='exerciseplan',
            name='exercise',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.exercise'),
        ),
    ]
