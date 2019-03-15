from rest_framework import serializers

from basicpayment.accounts.models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('balance', 'updated_at', 'owner', 'currency')


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('source_account', 'destination_account', 'amount',)

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)


