from django.db import models

from api.models.pet_and_breed import Breed
from api.models.user import BaseModel
from api.utils.helper import unique_id


def product_id():
    return unique_id(Product)


class Product(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, default=product_id)
    name = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    sub_category = models.ForeignKey(Breed, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_approved_status(self):
        if self.is_approved:
            return 'Approved'
        return 'Not Approved'
    