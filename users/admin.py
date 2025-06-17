from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админ-панель для пользователей."""
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'followers_count',
        'following_count',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)

    def followers_count(self, obj):
        return obj.following.count()
    followers_count.short_description = 'Подписчиков'

    def following_count(self, obj):
        return obj.follower.count()
    following_count.short_description = 'Подписок'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админ-панель для подписок."""
    list_display = ('user', 'author')
    search_fields = ('user__username', 'author__username')
    list_filter = ('user', 'author')
    ordering = ('user', 'author') 