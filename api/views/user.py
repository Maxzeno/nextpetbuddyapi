from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from api import serializers, models
from rest_framework import status
from rest_framework.response import Response

from api.utils.helper import convert_drf_form_error_to_norm

from rest_framework import reverse, status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives

from decouple import config


from drf_spectacular.utils import extend_schema

from api import serializers


@extend_schema(tags=['User'])
class UserViewSet(ModelViewSet):
    def get_serializer(self, *args, **kwargs):
        if hasattr(self, 'action') and self.action == 'create':
            self.serializer_class = serializers.UserPostSerializer
        else:
            self.serializer_class = serializers.UserSerializer

        return super().get_serializer(*args, **kwargs)


    def get_queryset(self):
        queryset = models.User.objects.all()
        return queryset

    def get_authenticators(self):
        if hasattr(self, 'action') and self.action == 'create':
            self.authentication_classes = []
        return [authentication_class() for authentication_class in self.authentication_classes]

    def get_permissions(self):
        if hasattr(self, 'action') and self.action == 'create':
            return []
        return [permission_class() for permission_class in self.permission_classes]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            base_url = config('FRONTEND_BASE_URL')
            reset_url = f"{base_url}{reverse.reverse('confirm_email', kwargs={'uid': uid, 'token': token}).replace('/api/v1', '')}"

            try:
                msg = EmailMultiAlternatives(
                    'Email Confirmation',
                    f'Click the following link to confirm your email: {reset_url}',
                    config('EMAIL_HOST_USER'),
                    [user.email]
                )
                msg.send()
            except ConnectionRefusedError as e:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': convert_drf_form_error_to_norm(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)