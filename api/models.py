from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'

    electricity = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Электричество')
    pulse = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Пульс')
    coin_balance = models.DecimalField(max_digits=30, decimal_places=20, verbose_name='Монет')


class Post(models.Model):
    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Пост'

    title = models.TextField(verbose_name='Название')
    body = models.TextField(verbose_name='Тело поста')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'

    body = models.TextField(verbose_name='Тело комментария')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(default=timezone.now)


class Grade(models.Model):
    class Meta:
        verbose_name = 'Оценки'
        verbose_name_plural = 'Оценка'

    grader = models.ForeignKey(to=User, verbose_name='Кто поставил', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    post = models.ForeignKey(to=Post, verbose_name='Пост', on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, verbose_name='Комментарий', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Advert(models.Model):
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламное объявление'

    url = models.URLField()
    image = models.URLField()
    view_count = models.PositiveIntegerField()