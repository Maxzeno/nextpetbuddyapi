
from api.utils.helper import unique_id
from api.models.user import BaseModel, User
from api.models.product import Product

from django.db import models


def order_id():
    return unique_id(Order)


class OrderItem(BaseModel):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_size = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    checked_out = models.BooleanField(default=False)
    price_ordered_at = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def paid_check_out(self):
        self.checked_out = True

        if not self.price_ordered_at:
            self.price_ordered_at = self.product.price
        self.save()

    def total_price(self):
        if self.price_ordered_at:
            return round(self.price_ordered_at * self.quantity, 2)
        return round(self.product.price * self.quantity, 2)

    def checked_out_status(self):
        if self.checked_out:
            return 'Yes'
        return 'No'

    def __str__(self):
        return f"{self.buyer.name} - {self.product.name} x {self.quantity} - checked out: {self.checked_out_status()}"



class Order(BaseModel):
    STATUS_CHOICES = [
        ('S', 'Success'),
        ('P', 'Pending'),
        ('C', 'Cancel'),
    ]

    id = models.CharField(primary_key=True, max_length=10, default=order_id)
    payment_ref = models.CharField(max_length=100, null=True, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    has_paid = models.BooleanField(default=False)
    incomplete_payment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.has_paid:
            # i thing we have an issue here which happens when we try to create order from admin
            for item in self.items.all():
                item.paid_check_out()

        super().save(*args, **kwargs)

    def get_total_price_now(self):
        price = 0
        for item in self.items.all():
            price += item.total_price()
        return price

    def order_status(self):
        for i in self.STATUS_CHOICES:
            if i[0].upper() == self.status.upper():
                return i[1]
        return ''

    def has_paid_status(self):
        if self.has_paid:
            return 'Yes'
        return 'No'

    def __str__(self):
        return f"{self.id}"

