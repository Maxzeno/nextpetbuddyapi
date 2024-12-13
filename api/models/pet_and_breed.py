
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.models.user import BaseModel


class Pet(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/pet/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Peties'


class Breed(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/breed/', blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="breeds")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Breeds'

        constraints = [
            models.UniqueConstraint(
                fields=['pet', 'name'],
                name='unique_name_per_pet'
            )
        ]
