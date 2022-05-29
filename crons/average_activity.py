from api.models import User
from random import randrange


# 0 0 * * 1
def give_electricity_and_coins_to_higher_than_average_activity():
    """Гарантируется выдача тем, к кого активность выше среднего по всем пользователям"""
    for user in User.objects.filter(pulse__gte=50):
        user.set_electricity(user.electricity + 20)  # TODO: remove hardcode
        user.set_coin(user.coin_balance + 10)  # TODO: remove hardcode


# 0 0 * * 1
def give_electricity_and_coins_to_lower_than_average_activity():
    """Рандомная выдача всем"""
    for user in User.objects.order_by('?')[:User.objects.all().count() // 2]:
        if randrange(10) == 0:
            user.set_electricity(user.electricity + 20)  # TODO: remove hardcode
        if randrange(10) == 1:
            user.set_coin(user.coin_balance + 10)  # TODO: remove hardcode
