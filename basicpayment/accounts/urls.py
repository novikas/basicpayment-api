from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register('accounts', views.AccountsViewSet, 'accounts')

urlpatterns = router.urls
