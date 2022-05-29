from django.db import models

# Create your models here.
from django.utils import timezone

from api.models import User


class Lot(models.Model):
    seller = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount_electricity = models.DecimalField(max_digits=10, decimal_places=5, verbose_name='Электричество', default=0)
    amount_coins = models.DecimalField(max_digits=30, decimal_places=20, verbose_name='Монет', default=0)
    buyer = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='buyer', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(default=timezone.now)

    is_committed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def buy_lot(self, buyer):
        if buyer.coin_balance >= self.amount_coins:
            # TODO: smart contract
            buyer.set_coin(self.buyer.coin_balance - self.amount_coins)
            self.seller.set_coin(self.seller.coin_balance + self.amount_coins)

            buyer.set_electricity(self.buyer.electricity + self.amount_electricity)
            self.seller.set_electricity(self.seller.electricity - self.amount_electricity)

            self.closed_at = timezone.now()
            self.is_closed = True
            self.is_committed = True

            buyer.save()
            self.save()

            return {'status': 'OK'}
        return {'status': 'Error', 'Error': 'not enough coins'}
