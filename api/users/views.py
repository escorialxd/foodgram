from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import AvatarSerializer, SubscriptionListSerializer, UserProfileSerializer
from users.models import Subscription, User


class CreateUserViewSet(UserViewSet):
    """UserViewSet that restricts user creation."""

    def create(self, request, *args, **kwargs):
        """Override create method to prevent user creation by regular users."""
        return Response(
            {"detail": "User creation is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['put', 'delete', 'get'], url_path='me/avatar', permission_classes=[IsAuthenticated])
    def avatar(self, request):
        user = request.user
        if request.method == 'PUT':
            serializer = AvatarSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'GET':
            serializer = AvatarSerializer(user)
            return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        user = request.user
        if request.method == 'POST':
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response({'errors': 'Вы уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)
            if user == author:
                return Response({'errors': 'Нельзя подписаться на себя'}, status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(user=user, author=author)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            sub = Subscription.objects.filter(user=user, author=author)
            if sub.exists():
                sub.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'errors': 'Вы не подписаны'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='subscriptions', permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user).select_related('author')
        serializer = SubscriptionListSerializer(subscriptions, many=True)
        return Response(serializer.data)
