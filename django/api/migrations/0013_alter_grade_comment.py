# Generated by Django 4.0.4 on 2022-05-28 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_post_rating_alter_post_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.comment', verbose_name='Комментарий'),
        ),
    ]
