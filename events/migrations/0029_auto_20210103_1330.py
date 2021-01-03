# Generated by Django 3.1.4 on 2021-01-03 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20210103_0521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 3, 23, 59, 10, 670819), verbose_name='Final time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 3, 0, 0, 10, 670819), verbose_name='Starting time'),
        ),
    ]