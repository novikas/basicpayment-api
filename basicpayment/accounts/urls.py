from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register('transactions', views.TransactionsViewSet, 'transactions')
router.register('', views.AccountsViewSet, 'accounts')

urlpatterns = router.urls
