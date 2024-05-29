from rest_framework import serializers
from api import models


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    user_address = AddressSerializer(many=False, read_only=True)
    
    class Meta:
        depth = 2
        model = models.User
        exclude = ('groups', 'user_permissions', 'last_login')
        extra_kwargs = {
            'email': {'read_only': True},
            'email_confirmed': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_suspended': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_active': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'password': {'write_only': True},
        }


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = models.User
        exclude = ('groups', 'user_permissions', 'last_login')
        extra_kwargs = {
            'email_confirmed': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_suspended': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_active': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'password': {'write_only': True},
        }

class UserAndTokenSerializer(UserPostSerializer):
    token = serializers.CharField()
