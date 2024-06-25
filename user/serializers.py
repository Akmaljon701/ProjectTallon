from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from user.models import CustomUser


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'password', 'branch')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        instance = super().update(instance, validated_data)
        return instance


class CustomUserGetSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'username', 'branch')
