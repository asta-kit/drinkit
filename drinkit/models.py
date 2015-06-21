from django.db import models
from decimal import Decimal
from datetime import date

class Drink(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('price',)

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

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ('firstname', 'lastname')

class Transaction(models.Model):
    drinker = models.ForeignKey(Drinker)
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    comment = models.CharField(blank=True, max_length=255)
    reckoning = models.ManyToManyField(Drink, through='Consumption')

    def __str__(self):
        return '{} -> {}: {} € — {}'.format(self.date, self.drinker, self.amount, self.comment)

    def save(self, *args, **kwargs):
        consumption = self.consumption_set.all()
        if len(consumption):
            self.amount = Decimal(0)
            for c in consumption:
                self.amount -= c.count * c.drink.price
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('-date', 'drinker')

class Consumption(models.Model):
    drink = models.ForeignKey(Drink)
    transaction = models.ForeignKey(Transaction)
    count = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        self.transaction.save()
        return res

    class Meta:
        unique_together = ('drink', 'transaction')
