# Generated by Django 4.0.4 on 2022-05-28 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='user',
            name='coin_balance',
            field=models.DecimalField(decimal_places=20, default=0, max_digits=30, verbose_name='Монет'),
        ),
        migrations.AlterField(
            model_name='user',
            name='electricity',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10, verbose_name='Электричество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='pulse',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=10, verbose_name='Пульс'),
        ),
    ]
