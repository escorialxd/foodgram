from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'', CreateUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/subscriptions/', CreateUserViewSet.as_view({'get': 'subscriptions'}), name='subscriptions'),
    path('users/<int:pk>/subscribe/', CreateUserViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'}), name='subscribe'),
    path('users/me/', CreateUserViewSet.as_view({'get': 'me', 'patch': 'partial_update'}), name='me'),
]
