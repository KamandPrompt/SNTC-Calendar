# Generated by Django 4.1.2 on 2022-10-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='club',
            field=models.CharField(max_length=100, null=True, verbose_name='Club name'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='email',
            field=models.CharField(max_length=100, verbose_name='Student Email'),
        ),
    ]