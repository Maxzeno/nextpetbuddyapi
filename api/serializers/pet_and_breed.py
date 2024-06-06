from rest_framework import serializers
from api import models


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Breed
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class PetSerializer(serializers.ModelSerializer):
    breeds = BreedSerializer(many=True, read_only=True)
    class Meta:
        model = models.Pet
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
