# Generated by Django 4.1.2 on 2022-11-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinationnote',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
