# Generated by Django 5.0.6 on 2024-05-25 12:11

import django.db.models.deletion
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=128)),
                ('id_photo', models.ImageField(upload_to='id_photos/')),
                ('injury', models.TextField()),
                ('pain_scale', models.IntegerField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=128)),
                ('license_id', models.CharField(max_length=50)),
                ('is_professional', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interested_in_notifications', models.BooleanField(default=True)),
                ('interested_in_calendar_sync', models.BooleanField(default=True)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to='myapp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('therapist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professional_details', to='myapp.therapist')),
            ],
        ),
        
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('Eid', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('videoUrl', models.CharField(max_length=100)),
                ('approval', models.BooleanField(default=False)),
                ('imgUrl', models.FileField(upload_to='exercise_images/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
