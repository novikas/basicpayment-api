from django.db import transaction
from rest_framework import viewsets, permissions, status, mixins

# Create your views here.
from rest_framework.response import Response

from basicpayment.accounts.models import Account, Transaction
from basicpayment.accounts.permissions import IsAccountOwner
from basicpayment.accounts.seriallizers import AccountSerializer, TransactionSerializer, TransactionCreateSerializer


class AccountsViewSet(viewsets.ModelViewSet):

    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)

    def get_permissions(self):
        action_permissions_mapping = {
            'create': (permissions.IsAuthenticated,),
            'list': (permissions.IsAuthenticated,),
            'retrieve': (permissions.IsAuthenticated, IsAccountOwner),
        }

        default = (permissions.AllowAny,)
        permissions_ = action_permissions_mapping.get(self.action, default)

        self.permission_classes = permissions_

        return super().get_permissions()


class TransactionsViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Transaction.objects.filter(account__owner=self.request.user)

    def get_permissions(self):
        action_permissions_mapping = {
            'create': (permissions.IsAuthenticated,),
            'list': (permissions.IsAuthenticated,),
            'retrieve': (permissions.IsAuthenticated,),
        }

        default = (permissions.AllowAny,)
        permissions_ = action_permissions_mapping.get(self.action, default)

        self.permission_classes = permissions_

        return super().get_permissions()

    def get_serializer_class(self):
        default_serializer = TransactionSerializer

        action_serializer_mapping = {
            'create': TransactionCreateSerializer,
            'list': TransactionSerializer,
            'retrieve': TransactionSerializer,
        }

        return action_serializer_mapping.get(self.action, default_serializer)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

