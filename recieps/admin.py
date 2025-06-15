from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
    Subscription,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Административная панель пользователей."""

    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("username", "email")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Административная панель рецептов."""

    list_display = ("name", "author", "cooking_time", "pub_date")
    search_fields = ("name", "author__username", "tags__name")
    list_filter = ("author", "tags", "pub_date")
    readonly_fields = ("pub_date",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная панель тегов."""

    list_display = ("name", "color", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель ингредиентов."""

    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Административная панель ингредиентов в рецепте."""

    list_display = ("recipe", "ingredient", "amount")
    search_fields = ("recipe__name", "ingredient__name")
    list_filter = ("recipe", "ingredient")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная панель избранного."""

    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user", "recipe")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Административная панель списка покупок."""

    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
    list_filter = ("user", "recipe")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Административная панель подписок."""

    list_display = ("user", "author")
    search_fields = ("user__username", "author__username")
    list_filter = ("user", "author")
