from rest_framework import serializers
from api import models


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields = '__all__'
        extra_kwargs = {
            'is_resolved': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

