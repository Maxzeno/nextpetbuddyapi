from rest_framework import generics
from api.views import models
from api.views import serializers


class ContactUsCreateView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = models.ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer
    

class EmailCreateView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = models.Email.objects.all()
    serializer_class = serializers.EmailSerializer