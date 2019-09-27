# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-27 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.CharField(blank=True, help_text='the name of your club', max_length=100, null=True, verbose_name='Club name'),
        ),
    ]
