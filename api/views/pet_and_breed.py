from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from api.views import models
from api.views import serializers
from rest_framework import filters


class PetListView(generics.ListAPIView):
    queryset = models.Pet.objects.all()
    serializer_class = serializers.PetSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['created_at']
    

class BreedListView(generics.ListAPIView):
    queryset = models.Breed.objects.all()
    serializer_class = serializers.BreedSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['created_at']
