# Generated by Django 4.1.2 on 2022-10-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_subscription_club_alter_subscription_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='email',
            new_name='student_email',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='club',
        ),
        migrations.AddField(
            model_name='event',
            name='created_by_email',
            field=models.CharField(blank=True, max_length=100, verbose_name='Email of Creator'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='club_email',
            field=models.CharField(default='b19188@students.iitmandi.ac.in', max_length=100, verbose_name='Club name'),
            preserve_default=False,
        ),
    ]
