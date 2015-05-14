from django.db import models

class Drink(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)

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

    def __str__(self):
        return self.fullname

class Transaction(models.Model):
    drinker = models.ForeignKey(Drinker)
    date = models.DateField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    reckoning = models.ManyToManyField(Drink, through='Consumption')

class Consumption(models.Model):
    drink = models.ForeignKey(Drink)
    transaction = models.ForeignKey(Transaction)
    count = models.PositiveSmallIntegerField()
