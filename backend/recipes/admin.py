from django.contrib import admin
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    Favorite,
    ShoppingCart,
)


class RecipeIngredientInline(admin.TabularInline):
    """Inline for ingredients in recipe."""

    model = RecipeIngredient
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin panel."""

    list_display = ("name", "color", "slug")
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient admin panel."""

    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe admin panel."""

    list_display = (
        "name",
        "author",
        "cooking_time",
        "favorites_count",
    )
    search_fields = ("name", "author__username", "tags__name")
    list_filter = ("author", "tags")
    inlines = (RecipeIngredientInline,)
    empty_value_display = "<пусто>"

    def favorites_count(self, obj):
        return obj.favorites.count()

    favorites_count.short_description = "Favorites count"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favorite admin panel."""

    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Shopping cart admin panel."""

    list_display = ("user", "recipe")
    search_fields = ("user__username", "recipe__name")
