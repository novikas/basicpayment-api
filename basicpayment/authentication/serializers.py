
from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

from basicpayment.accounts.models import Account
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
        Account.objects.bulk_create(accounts)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'accounts')