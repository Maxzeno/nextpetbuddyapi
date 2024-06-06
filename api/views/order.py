from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema
from api import serializers, models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


@extend_schema(tags=['Cart'])
class OrderItemViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    filterset_fields = ['buyer__id', 'animal__id']
    
    
    def get_serializer(self, *args, **kwargs):
        if hasattr(self, 'action') and self.action == 'create':
            self.serializer_class = serializers.OrderItemPostSerializer
        else:
            self.serializer_class = serializers.OrderItemSerializer

        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = request.data
        user = request.user

        if data.get('buyer') != user.id:
            return Response({'detail': 'Buyer is not the currently the authenticated user'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        query = queryset.filter(buyer=user, animal_id=serializer.validated_data.get('animal'), order__isnull=True)
        if query:
            query = query.first()
            query.quantity += 1
            query.save()
            print(query.quantity)
            serializer = self.get_serializer(query)
            print(serializer.data)
        else:
            self.perform_create(serializer)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def get_queryset(self):
        user = self.request.user
        return models.OrderItem.objects.filter(buyer=user)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        exists = models.OrderItem.objects.filter(id=instance.id, order__isnull=False)
        if exists:
            raise ValidationError({'detail': 'This order item cannot be deleted.'})

        instance.delete()
        return Response({'detail': 'Cart item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        
    def get_queryset(self):
        queryset = models.OrderItem.objects.all()
        return queryset


@extend_schema(tags=['Order'])
class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    
    def get_serializer(self, *args, **kwargs):
        if hasattr(self, 'action') and self.action == 'create':
            self.serializer_class = serializers.OrderPostSerializer
        else:
            self.serializer_class = serializers.OrderSerializer

        return super().get_serializer(*args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if data.get('buyer') != user.id:
            return Response({'detail': 'Buyer is not the currently the authenticated user'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        orderitems = models.OrderItem.objects.filter(buyer=user, order__isnull=True)
        order = models.Order.objects.create(buyer=user, items=orderitems)
        serializer = self.get_serializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.user

        queryset = queryset.filter(buyer=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        queryset = models.Order.objects.all()
        return queryset
