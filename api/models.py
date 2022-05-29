from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'

    electricity = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Электричество', default=0)
    pulse = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Пульс', default=0)
    coin_balance = models.DecimalField(max_digits=30, decimal_places=20, verbose_name='Монет', default=0)
    last_time_gained_pulse = models.DateTimeField(default=timezone.now)
    day_visited_in_a_row = models.PositiveIntegerField(default=1)

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def _correct_pulse(self):
        if self.pulse > 100:
            self.pulse = 100
            self.save()

    def set_pulse(self, pulse_amount):
        """Сеттер пульса пользователя"""
        self.pulse = pulse_amount
        self.save()
        self._correct_pulse()

    def set_electricity(self, electricity_amount):
        """Сеттер энергии пользователя"""
        self.electricity = electricity_amount
        self.save()

    def get_user_weight_for_grading(self) -> Decimal:
        """Получить значение рейтинга от 0 до 2 исходя из пульса пользователя"""
        return Decimal(0.02) * self.pulse


class Post(models.Model):
    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Пост'

    slug = models.SlugField(unique=True)
    title = models.TextField(verbose_name='Название')
    body = models.TextField(verbose_name='Тело поста')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.s = slugify(self.title)

        super(Post, self).save(*args, **kwargs)

    def count_likes_on_post(self):
        return Grade.objects.filter(post=self, is_like=True).count()

    def count_dislikes_on_post(self):
        return Grade.objects.filter(post=self, is_dislike=True).count()

    def set_calculated_rating(self):
        self.rating = self.count_likes_on_post() + self.count_dislikes_on_post()
        self.save()

    def add_post(self, title: str, body: str, author: User):
        self.title = title
        self.body = body
        self.author = author
        self.save()
        author.set_pulse(author.pulse + 20)  # TODO: remove hardcode


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'

    body = models.TextField(verbose_name='Тело комментария')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name='Пост', null=True, blank=True)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def comment_post(self, post: Post, author: User, comment_body: str):
        """Добавить комментарий на пост"""
        self.post = post
        self.author = author
        self.body = comment_body
        self.save()
        author.set_pulse(author.pulse + 10)  # TODO: remove hardcode

    def count_likes(self):
        return Grade.objects.filter(comment=self, is_like=True).count()

    def count_dislikes(self):
        return Grade.objects.filter(comment=self, is_dislike=True).count()

    def set_calculated_rating(self):
        self.rating = self.count_likes() + self.count_dislikes()
        self.save()


class Grade(models.Model):
    class Meta:
        verbose_name = 'Оценки'
        verbose_name_plural = 'Оценка'

    grader = models.ForeignKey(to=User, verbose_name='Кто поставил', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)
    is_dislike = models.BooleanField(default=False)
    post = models.ForeignKey(to=Post, verbose_name='Пост', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(to=Comment, verbose_name='Комментарий', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_likes_on_comment(self, comment):
        return self.objects.filter(is_like=True, comment=comment).count()

    def get_dislikes_on_comment(self, comment):
        return self.objects.filter(is_dislike=True, comment=comment).count()

    def _vote_for_post_or_comment(self, user: User, is_like: bool, is_dislike: bool,
                                  post: Post = None, comment: Comment = None) -> bool:
        """return is_success"""
        if post and comment:
            raise Exception('post and comment not None error')
        if is_like and is_dislike:
            raise Exception('is_like and is_dislike True error')
        if post:
            if Grade.objects.filter(grader=user, post=post).count() >= 1:
                return False
        if comment:
            if Grade.objects.filter(grader=user, comment=comment).count() >= 1:
                return False
        self.is_like = is_like
        self.is_dislike = is_dislike
        self.grader = user
        self.post = post
        self.comment = comment
        self.grader.electricity = -1  # TODO: remove hardcode
        if post:
            _effect_on_the_author = Decimal(0.5) * \
                                    self.post.author.get_user_weight_for_grading()  # TODO: remove hardcode
        if comment:
            _effect_on_the_author = Decimal(0.5) * \
                                    self.comment.author.get_user_weight_for_grading()  # TODO: remove hardcode
        if is_dislike:
            _effect_on_the_author *= -1  # TODO: remove hardcode
        if post:
            self.post.set_calculated_rating()
            self.post.author.set_electricity(self.post.author.electricity + _effect_on_the_author)
        if comment:
            self.comment.set_calculated_rating()
            self.comment.author.set_electricity(self.comment.author.electricity + _effect_on_the_author)

        self.save()
        user.set_pulse(user.pulse + 10)  # TODO: remove hardcode
        return True

    def like_post(self, user: User, post: Post):
        """Лайкнуть пост"""
        return self._vote_for_post_or_comment(user, is_like=True, is_dislike=False, post=post)

    def dislike_post(self, user: User, post: Post):
        """Дизлайкнуть пост"""
        return self._vote_for_post_or_comment(user, is_like=False, is_dislike=True, post=post)

    # def cancel_vote_post(self, user: User, post: Post):
    #     """Отменить лайк/дизлайк на пост"""
    #     self._vote_for_post_or_comment(user, is_like=False, is_dislike=False, post=post)

    def like_comment(self, user: User, comment: Comment):
        """Лайкнуть комментарий"""
        return self._vote_for_post_or_comment(user, is_like=True, is_dislike=False, comment=comment)

    def dislike_comment(self, user: User, comment: Comment):
        """Дизлайкнуть комментарий"""
        return self._vote_for_post_or_comment(user, is_like=False, is_dislike=True, comment=comment)

    # def cancel_vote_comment(self, user: User, comment: Comment):
    #     """Отменить лайк/дизлайк на комментарий"""
    #     self._vote_for_post_or_comment(user, is_like=False, is_dislike=False, comment=comment)


class Advert(models.Model):
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламное объявление'

    url = models.URLField()
    image = models.URLField()
    view_count = models.PositiveIntegerField()

    def add_advert(self, url: str, image: str):
        """Добавить рекламный баннер"""
        self.url = url
        self.image = image
        self.save()
        # TODO: надо добавить пользователя, который добавляет рекламу, и списывать с этого пользователя энергию,
        #  затрачиваемую за размещение
