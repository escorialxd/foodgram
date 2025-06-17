from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .fields import Base64ImageField
from .models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Favorite,
    ShoppingCart,
)

User = get_user_model()


class TokenCreateSerializer(serializers.Serializer):
    """Сериализатор создания токена."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                "Пожалуйста, укажите email и пароль"
            )

        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if not user:
            raise serializers.ValidationError("Неверный email или пароль")

        attrs["user"] = user
        return attrs


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "avatar",
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        )
        read_only_fields = ("id",)

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(
        source="recipe_ingredients", many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_author(self, obj):
        from api.users.serializers import CustomUserSerializer
        return CustomUserSerializer(obj.author, context=self.context).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""

    ingredients = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def to_representation(self, instance):
        """Преобразование объекта в словарь для ответа."""
        return RecipeSerializer(instance, context=self.context).data

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)

        for ingredient_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data.get("id"),
                amount=ingredient_data.get("amount"),
            )
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" in validated_data:
            ingredients_data = validated_data.pop("ingredients")
            instance.ingredients.clear()
            for ingredient_data in ingredients_data:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient_id=ingredient_data.get("id"),
                    amount=ingredient_data.get("amount"),
                )
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            instance.tags.set(tags_data)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=("user", "recipe"),
                message="Рецепт уже в избранном",
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=("user", "recipe"),
                message="Рецепт уже в списке покупок",
            )
        ]
