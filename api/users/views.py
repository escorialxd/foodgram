from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet


class CreateUserViewSet(UserViewSet):
    """UserViewSet that restricts user creation."""

    def create(self, request, *args, **kwargs):
        """Override create method to prevent user creation by regular users."""
        return Response(
            {"detail": "User creation is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
