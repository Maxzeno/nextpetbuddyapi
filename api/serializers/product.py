# serializers/product.py
from rest_framework import serializers
from api.models import Animal
from api.serializers.order import OrderItemSerializer

class ProductSerializer(serializers.ModelSerializer):
    orderitem = serializers.SerializerMethodField()

    class Meta:
        model = Animal  # Ensure this is the correct model name
        depth = 2
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_orderitem(self, obj):
        request = self.context.get('request', None)
        if not request or not request.user.is_authenticated:
            return None
        order_item = obj.order_items.filter(order__isnull=True).first()
        if order_item:
            return OrderItemSerializer(order_item).data
        return None
