# Generated by Django 2.2.5 on 2019-09-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20190928_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.CharField(help_text='the name of your club', max_length=100, null=True, verbose_name='Club name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.TextField(help_text='Describe your event', null=True, verbose_name='Name fo the Event'),
        ),
    ]