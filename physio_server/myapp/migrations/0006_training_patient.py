# Generated by Django 5.0.6 on 2024-05-31 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_training_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='patient',
            field=models.ForeignKey(default='NULL', on_delete=django.db.models.deletion.CASCADE, to='myapp.patient'),
        ),
    ]
