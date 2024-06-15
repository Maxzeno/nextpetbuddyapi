from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser


class MyNoAuth(BaseAuthentication):
    def authenticate(self, request):
        return (AnonymousUser(), None)
    