from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Subscription

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """User admin panel."""
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

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def followers_count(self, obj):
        return obj.following.count()
    followers_count.short_description = 'Followers'

    def following_count(self, obj):
        return obj.follower.count()
    following_count.short_description = 'Following'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Subscription admin panel."""
    list_display = ('user', 'author')
    search_fields = ('user__username', 'author__username')
    list_filter = ('user', 'author')
    ordering = ('user', 'author')
