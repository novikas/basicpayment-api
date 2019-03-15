from rest_framework import viewsets, permissions

# Create your views here.
from basicpayment.accounts.models import Account, Transaction
from basicpayment.accounts.permissions import IsAccountOwner
from basicpayment.accounts.seriallizers import AccountSerializer


class AccountsViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
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


class TransactionsViewSet(viewsets.ModelViewSet):

    queryset = Transaction.objects.all()
    serializer_class = Trans

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

