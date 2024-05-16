from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    detail = serializers.CharField()


class MessageDataSerializer(serializers.Serializer):
    detail = serializers.CharField()
    data = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_again = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password_again = serializers.CharField()
