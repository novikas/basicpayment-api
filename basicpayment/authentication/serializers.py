
from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

from basicpayment.accounts.models import Account, Transaction
from basicpayment.accounts.seriallizers import AccountSerializer


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        accounts = [
            Account(currency=currency_name, owner=user) for currency_name, currency_data in settings.CURRENCIES.items()
        ]

        for acc in accounts:
            acc.save()

        usd_account = next(acc for acc in accounts if acc.currency == 'USD')
        Transaction.create_debt(usd_account, 100)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'accounts')
