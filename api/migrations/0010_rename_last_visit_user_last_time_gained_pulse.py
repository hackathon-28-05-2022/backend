# Generated by Django 4.0.4 on 2022-05-28 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_last_visit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_visit',
            new_name='last_time_gained_pulse',
        ),
    ]
