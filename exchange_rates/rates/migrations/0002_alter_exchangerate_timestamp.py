# Generated by Django 5.1.4 on 2024-12-07 17:01

import rates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='timestamp',
            field=models.DateTimeField(default=rates.models.get_default_time),
        ),
    ]