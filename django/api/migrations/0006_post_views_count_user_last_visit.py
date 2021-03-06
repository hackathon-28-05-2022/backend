# Generated by Django 4.0.4 on 2022-05-28 21:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_comment_rating_alter_grade_post_alter_post_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_visit',
            field=models.DateField(default=datetime.datetime(2022, 5, 28, 21, 30, 12, 49067, tzinfo=utc), verbose_name=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
