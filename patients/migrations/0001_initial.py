# Generated by Django 4.1.2 on 2022-11-04 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('home_address', models.CharField(max_length=500)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ExaminationNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('text', models.TextField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examination_notes', to='patients.patientcard')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='examination_notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
