from django.contrib import admin
from api import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Address)
admin.site.register(models.Pet)
admin.site.register(models.Breed)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Animal)
admin.site.register(models.ContactUs)
admin.site.register(models.Email)
