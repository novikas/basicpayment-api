from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

from basicpayment.common.currency import Currency

currencies = settings.CURRENCIES


class Account(models.Model):

    currency_choices = [
        (name, name) for name, val in currencies.items()
    ]

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2, default=0,
        verbose_name=_('account balance')
    )

    currency = models.CharField(
        max_length=5,
        choices=currency_choices,
        verbose_name=_('account currency')
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='accounts',
        verbose_name=_('account owner')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def has_available(self, amount):
        balance_currency = Currency(self.balance, self.currency)
        amount_currency = Currency(amount, self.currency)
        return balance_currency >= amount_currency

    @property
    def is_banker(self):
        return self.owner.username == settings.BANKER_CREDENTIALS['username']

    @property
    def balance_multicurrency(self):
        return Currency(self.balance, self.currency)


class Transaction(models.Model):

    TYPE_DEBT = 0
    TYPE_CREDIT = 1

    transaction_types = [
        (TYPE_DEBT, 'DEBT'),
        (TYPE_CREDIT, 'CREDIT'),
    ]

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name=_('transaction amount')
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name=_('account')
    )

    type = models.CharField(max_length=10, choices=transaction_types, null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
