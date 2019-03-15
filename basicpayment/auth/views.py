from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework_simplejwt.state import User

from basicpayment.auth.serializers import SignUpSerializer, UserDetailSerializer


class SignUpViewSet(
            mixins.CreateModelMixin,
            viewsets.GenericViewSet
        ):

    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(
            mixins.RetrieveModelMixin,
            mixins.ListModelMixin,
            viewsets.GenericViewSet
        ):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
