from django.contrib import admin
from django.db import models

from .models import Drink, Drinker, Transaction, Consumption

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'active')


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0

class BalanceFilter(admin.SimpleListFilter):
    title = 'Balance less than'
    parameter_name = 'balance'
    def lookups(self, request, model_admin):
        return ((-500,-500), (-100,-100), (-50,-50), (0,0))
    def queryset(self, request, queryset):
        if self.value():
            return queryset.annotate(_balance=models.Sum('transaction__amount')).filter(_balance__lt=self.value())

@admin.register(Drinker)
class DrinkerAdmin(admin.ModelAdmin):
    inlines = (TransactionInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(_balance=models.Sum('transaction__amount'))
        return qs

    def balance(self, drinker):
        return drinker._balance
    balance.admin_order_field = '_balance'

    list_display = ('firstname', 'lastname', 'balance', 'active')
    list_filter = ('active', BalanceFilter)
    search_fields = ('firstname', 'lastname', 'email')


class ConsumptionInline(admin.TabularInline):
    model = Consumption
    extra = 0

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    inlines = (ConsumptionInline,)
    list_display = ('drinker', 'date', 'amount')
    date_hierarchy = 'date'
