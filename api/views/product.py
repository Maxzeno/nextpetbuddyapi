from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from api.views import models
from api.views import serializers
from rest_framework import filters


class ProductListView(generics.ListAPIView):
    queryset = models.Animal.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['created_at']
    