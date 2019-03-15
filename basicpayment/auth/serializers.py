
from rest_framework import serializers
from django.contrib.auth.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'accounts', )
