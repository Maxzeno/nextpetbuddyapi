from rest_framework import serializers
from api import models


class OrderItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'
        extra_kwargs = {
            'checked_out': {'read_only': True},
            'price_ordered_at': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = models.OrderItem
        fields = '__all__'
        extra_kwargs = {
            'buyer': {'read_only': True},
            'animal': {'read_only': True},
            'checked_out': {'read_only': True},
            'price_ordered_at': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
        
class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'paid': {'read_only': True},
            'status': {'read_only': True},
            'delivery_fee': {'read_only': True},
            'has_paid': {'read_only': True},
            'incomplete_payment': {'read_only': True},
            'items': {'read_only': True},
            'payment_ref': {'read_only': True},
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
