from decimal import Decimal

from django.conf.urls import url
from django.contrib import admin, messages
from django.core.mail import send_mass_mail
from django.db import models
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .models import Drink, Drinker, Transaction, Consumption

class BaseReckoningFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Drinker.objects.filter(active=True)

    def add_fields(self, form, index):
        super().add_fields(form, index)
        for drink in Drink.objects.filter(active=True):
            form.fields['drink{}'.format(drink.pk)] = \
                forms.IntegerField(min_value=0, required=False)

ReckoningFormSet = modelformset_factory(
    Drinker,
    fields=('firstname', 'lastname', 'email', 'active'),
    extra=15,
    formset=BaseReckoningFormSet,
)

class DrinkitAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^drinkit/reckoning/$', self.admin_view(self.reckoning_view), name='reckoning'),
        ]
        return my_urls + urls

    def reckoning_view(self, request):
        params = {}
        params['title'] = 'Abrechnung'
        params['drinks'] = Drink.objects.filter(active=True)
        if request.method == 'POST':
            formset = ReckoningFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    if not form.has_changed():
                        continue
                    form.save()
                    transaction = form.instance.transaction_set.create(amount=Decimal(0))
                    for drink in params['drinks']:
                        count = form.cleaned_data['drink{}'.format(drink.pk)]
                        if not count:
                            continue

                        consumption = Consumption(
                            drink=drink,
                            transaction=transaction,
                            count=count,
                        )
                        consumption.save()

                messages.success(request, 'Abrechnung erfolgreich.')

                return HttpResponseRedirect('/admin/drinkit/drinker/')
        else:
            formset = ReckoningFormSet()

        params['formset'] = formset
        return render(request, 'admin/drinkit/reckoning.html', params)

admin_site = DrinkitAdminSite()

@admin.register(Drink, site=admin_site)
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

# Actions
def activate(modeladmin, request, queryset):
    for drinker in queryset:
        drinker.active = True
        drinker.save()

def deactivate(modeladmin, request, queryset):
    for drinker in queryset:
        drinker.active = False
        drinker.save()

def send_balance_email(modeladmin, request, queryset):
    emails = []
    template = loader.get_template('drinkit/balance_email.txt')

    for drinker in queryset:
        message = template.render({'drinker':drinker})
        emails.append((
            'AStA-Getränkeabrechnung',
            message,
            'getraenke@asta-kit.de',
            [drinker.email],
        ))

    num = send_mass_mail(emails)
    if num == len(emails):
        messages.success(request, 'E-Mails erfolgreich verschickt')
    else:
        messages.error(
            request,
            '{} E-Mails konnten nicht erfolgreich verschickt werden'.format(len(emails) - num),
        )

@admin.register(Drinker, site=admin_site)
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
    actions = (activate, deactivate, send_balance_email)


class ConsumptionInline(admin.TabularInline):
    model = Consumption
    extra = 0

@admin.register(Transaction, site=admin_site)
class TransactionAdmin(admin.ModelAdmin):
    inlines = (ConsumptionInline,)
    list_display = ('drinker', 'date', 'amount')
    date_hierarchy = 'date'
