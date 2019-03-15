
from rest_framework import serializers
from django.contrib.auth.models import User

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

        accounts = Account.objects.bulk_create([
            Account(currency=Account.CURRENCY_USD, owner=user),
            Account(currency=Account.CURRENCY_CNY, owner=user),
            Account(currency=Account.CURRENCY_EUR, owner=user),
        ])

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('username', 'accounts', )
