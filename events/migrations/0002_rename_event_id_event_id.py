# Generated by Django 4.1.2 on 2022-10-08 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_id',
            new_name='id',
        ),
    ]
