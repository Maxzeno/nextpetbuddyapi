from rest_framework import serializers
from api import models


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
