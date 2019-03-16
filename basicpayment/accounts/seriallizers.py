from rest_framework import serializers
from django.conf import settings

from basicpayment.accounts.models import Account, Transaction
from basicpayment.common.currency import Currency


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'balance', 'updated_at', 'owner', 'currency')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('account', 'amount',)


class TransactionCreateSerializer(serializers.Serializer):
    from_account = serializers.IntegerField()
    to_account = serializers.IntegerField()
    # amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    amount = serializers.FloatField(min_value=0.01)

    class Meta:
        fields = ('from_account', 'to_account', 'amount')

    def validate(self, data):
        if data['from_account'] == data['to_account']:
            raise serializers.ValidationError('from_account and to_account should be different')

        sender_account = Account.objects.get(pk=data['from_account'])
        receiver_account = Account.objects.get(pk=data['to_account'])

        if not sender_account:
            raise serializers.ValidationError('Account with id {} doesn\'t exist'.format(data['from_account']))
        if not receiver_account:
            raise serializers.ValidationError('Account with id {} doesn\'t exist'.format('to_account'))

        is_internal_transfer = sender_account.owner.id == receiver_account.owner.id
        amount = data['amount'] if is_internal_transfer else data['amount'] * (1 + settings.SERVICE_FEE)
        is_enough = sender_account.has_available(amount)

        if not is_enough:
            message = 'There are not enough funds to perform transaction.' \
                      + ('' if is_internal_transfer else 'Please consider that amount with service fee is {}'
                         .format(amount))

            raise serializers.ValidationError(message)

        return data

    def create(self, validated_data):
        sender_account = Account.objects.get(pk=validated_data['from_account'])
        amount_currency = Currency(validated_data['amount'], sender_account.currency)

        receiver_account = Account.objects.get(pk=validated_data['to_account'])
        is_internal_transfer = sender_account.owner.id == receiver_account.owner.id

        Transaction.create_credit(sender_account, amount_currency[sender_account.currency], not is_internal_transfer)
        Transaction.create_debt(receiver_account, amount_currency[receiver_account.currency])

        return validated_data





