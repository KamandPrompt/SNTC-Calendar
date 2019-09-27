# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-27 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20190927_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.TextField(blank=True, help_text='the name of your club', max_length=100, null=True, verbose_name='Club name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.TextField(blank=True, help_text='Describe your event', null=True, verbose_name='Name fo the Event'),
        ),
    ]
