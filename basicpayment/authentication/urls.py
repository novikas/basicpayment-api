from rest_framework import routers
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = routers.SimpleRouter()

router.register('sign-up', views.SignUpViewSet, 'sign-up')
router.register('users', views.UserViewSet, 'users')

urlpatterns = router.urls
urlpatterns += [
    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh$', TokenRefreshView.as_view(), name='token_refresh'),
]
