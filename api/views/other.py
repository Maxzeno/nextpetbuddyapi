from rest_framework import generics
from api.views import models
from api.views import serializers


class ContactUsCreateView(generics.CreateAPIView):
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer
    

class EmailCreateView(generics.CreateAPIView):
    queryset = models.Email.objects.all()
    serializer_class = serializers.EmailSerializer