from decimal import Decimal

from django.conf import settings


class Currency:
    amount = Decimal(0)

    currencies = settings.CURRENCIES

    def __init__(self, amount=Decimal(0), currency='USD'):
        self.set_amount(amount, currency)

    def set_amount(self, amount, currency):
        if currency not in self.currencies:
            raise ValueError('{} is not supported. Failed to convert'.format(currency))
        currency_info = self.currencies[currency]

        self.amount = Decimal(amount) * currency_info['usd_exchange_rate']

    def __add__(self, other):
        return Currency(self.amount + other.amount)

    def __sub__(self, other):
        return Currency(self.amount - other.amount)

    def __eq__(self, other):
        return self.amount == other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __ge__(self, other):
        return self.amount >= other.amount

    def __getitem__(self, currency):
        if currency not in self.currencies:
            raise ValueError('{} is not supported. Failed to convert'.format(currency))
        currency_info = self.currencies[currency]
        return self.amount / currency_info['usd_exchange_rate']

    def __str__(self):
        return '{} USD'.format(self.amount)
