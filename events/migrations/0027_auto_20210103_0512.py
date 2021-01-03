# Generated by Django 3.1.4 on 2021-01-02 23:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20210103_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 3, 23, 59, 47, 438446), verbose_name='Final time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 3, 0, 0, 47, 438446), verbose_name='Starting time'),
        ),
    ]