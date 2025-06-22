from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'', CreateUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
