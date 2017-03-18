# Drinkit – The drinker management used by the AStA at the KIT
#
# Written in 2015 by Michael Tänzer <neo@nhng.de>
#
# This stuff is beer-ware (CC0 flavour): If you meet one of the authors some
# day, and you think the stuff is worth it, you may buy them a beer in return,
# if you want to. Also you can do anything you want with the stuff (and we
# encourage that you do) because the stuff is formally licensed according to the
# following terms:
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with
# this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from django.db import models
from decimal import Decimal
from datetime import date

class Drink(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.name


class Drinker(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    @property
    def fullname(self):
        return self.firstname + ' ' + self.lastname

    email = models.EmailField()
    active = models.BooleanField(default=True)

    @property
    def balance(self):
        return self.transaction_set.aggregate(balance=models.Sum('amount'))['balance']
    @property
    def credit(self):
        return -self.balance

    class Meta:
        ordering = ('firstname', 'lastname')

    def __str__(self):
        return self.fullname


class Transaction(models.Model):
    drinker = models.ForeignKey(Drinker)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    comment = models.CharField(blank=True, max_length=255)
    reckoning = models.ManyToManyField(Drink, through='Consumption')

    class Meta:
        ordering = ('-date', 'drinker')

    def __str__(self):
        return '{} -> {}: {} € — {}'.format(self.date, self.drinker, self.amount, self.comment)

    def save(self, *args, **kwargs):
        consumption = self.consumption_set.all()
        if len(consumption):
            self.amount = Decimal(0)
            for c in consumption:
                self.amount -= c.count * c.drink.price
        return super().save(*args, **kwargs)


class Consumption(models.Model):
    drink = models.ForeignKey(Drink)
    transaction = models.ForeignKey(Transaction)
    count = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('drink', 'transaction')

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        self.transaction.save()
        return res
