from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from api.utils.auth import MyNoAuth
from api.views import models
from api.views import serializers
from rest_framework import filters
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Product'])
class ProductListViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = []
    queryset = models.Animal.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['created_at']
    filterset_fields = ['breed', 'breed__pet']
    
    def get_authenticators(self):
        return [*super().get_authenticators(), MyNoAuth()]
    