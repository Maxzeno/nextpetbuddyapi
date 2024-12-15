from rest_framework import serializers
from api import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

