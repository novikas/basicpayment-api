from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Account(models.Model):

    CURRENCY_USD = 'USD'
    CURRENCY_CNY = 'CNY'
    CURRENCY_EUR = 'EUR'

    currency_choices = [
        (CURRENCY_USD, CURRENCY_USD),
        (CURRENCY_CNY, CURRENCY_CNY),
        (CURRENCY_EUR, CURRENCY_EUR),
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


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name=_('transaction amount')
    )

    source_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='outcoming_transactions',
        verbose_name=_('source account')
    )

    source_currency = models.CharField(
        max_length=5,
        choices=Account.currency_choices,
        verbose_name=_('source currency')
    )

    destination_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='incoming_transactions',
        verbose_name=_('destination account')
    )

    destination_currency = models.CharField(
        max_length=5,
        choices=Account.currency_choices,
        verbose_name=_('source currency')
    )

    created_at = models.DateTimeField(auto_now_add=True)

