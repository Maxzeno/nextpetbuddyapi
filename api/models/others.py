from django.db import models

from api.models.user import BaseModel


class Email(BaseModel):
    email = models.EmailField(unique=True, null=False)

    def __str__(self):
        return self.email
    

class ContactUs(BaseModel):
    email = models.EmailField(unique=True)
    message = models.CharField(max_length=1000)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Contact us'
