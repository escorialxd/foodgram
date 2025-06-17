from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

User = get_user_model()


class UserListView(generics.ListCreateAPIView):
    """View for listing and creating users."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting users."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
