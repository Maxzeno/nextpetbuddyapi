from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from api import serializers, models


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
