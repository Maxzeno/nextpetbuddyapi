from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import generics, reverse, status, mixins, views
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.exceptions import InvalidToken

from decouple import config


from rest_framework.permissions import IsAuthenticated, BasePermission
from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from api import serializers
from api.serializers.auth import ChangePasswordSerializer
from api.serializers.user import UserSerializer
from api.utils.custom_status_code import HTTP_450_EMAIL_NOT_CONFIRMED


class NoPatchPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            return False
        return True


class UpdateOnlyAPIView(mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    """
    Concrete view for updating a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@extend_schema(tags=['Auth'], responses=serializers.UserSerializer)
class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            raise InvalidToken()

        if not user.is_active:
            return Response({'detail': "user is not active"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        access_token = serializer.validated_data.get('access')
        if access_token is None:
            raise InvalidToken()

        user_serializer = UserSerializer(user)
        data = user_serializer.data

        if not user.email_confirmed:
            return Response({'detail': "Email not confirmed", "data": user.id}, status=HTTP_450_EMAIL_NOT_CONFIRMED)

        data['token'] = access_token

        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'], responses=serializers.UserAndTokenSerializer)
class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        data = serializer.data
        data['token'] = request.META.get('HTTP_AUTHORIZATION', '').split()[-1]
        return Response(data)


@extend_schema(tags=['Auth'], responses=serializers.MessageSerializer)
class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = serializers.ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = get_user_model().objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            base_url = config('FRONTEND_BASE_URL')
            reset_url = f"{base_url}{reverse.reverse('password_reset', kwargs={'uid': uid, 'token': token}).replace('/api/v1', '')}"

            try:
                msg = EmailMultiAlternatives(
                    'Password Reset',
                    f'Click the following link to reset your password: {reset_url}',
                    config('EMAIL_HOST_USER'),
                    [email]
                )
                msg.send()
            except ConnectionRefusedError as e:
                return Response({'detail': 'An error accurred while tring to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': 'If an account with this email exists, a password reset email has been sent.'})


@extend_schema(tags=['Auth'], responses=serializers.MessageSerializer)
class PasswordResetView(UpdateOnlyAPIView):
    serializer_class = serializers.PasswordResetSerializer
    authentication_classes = ()
    permission_classes = ()

    def update(self, request, *args, **kwargs):
        token = kwargs.get('token')
        uid = kwargs.get('uid')
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.filter(pk=uid).first()

        if user and default_token_generator.check_token(user, token):
            password = request.data.get('password')
            password_again = request.data.get('password_again')
            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)
            if password != password_again:
                return Response({'detail': 'password and repeat does not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = password
            user.save()
            return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'], responses=serializers.MessageSerializer)
class SendConfirmEmailView(generics.GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('uid')
        user = get_user_model().objects.filter(pk=user_id).first()

        if user:
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
                return Response({'detail': 'An error accurred while tring to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': 'If an account with this email exists, a password confirmation email has been sent.'})


@extend_schema(tags=['Auth'], responses=serializers.MessageSerializer)
class ConfirmEmailView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        uid = kwargs.get('uid')
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_user_model().objects.filter(pk=uid).first()

        if user and default_token_generator.check_token(user, token):
            user.email_confirmed = True
            user.save()
            return Response({'detail': 'Email Confirmed'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid token or expired'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'], responses=serializers.MessageSerializer)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid()
        user = get_user_model().objects.filter(pk=request.user.id).first()
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')
        new_password_again = serializer.validated_data.get(
            'new_password_again')
        if not user.check_password(old_password):
            return Response({'detail': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            password_validation.validate_password(new_password)
        except ValidationError as e:
            return Response({'detail': e}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != new_password_again:
            return Response({'detail': 'Password and repeat does not match'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = new_password
        user.save()
        return Response({'detail': 'Password changed'}, status=status.HTTP_200_OK)
