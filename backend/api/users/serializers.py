from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscription
from recipes.fields import Base64ImageField
from api.recipes.short_serializers import ShortRecipeSerializer

User = get_user_model()


class TokenCreateSerializer(serializers.Serializer):
    """Token creation serializer."""

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

        self.user = user
        return attrs


class HybridImageField(Base64ImageField):
    def to_internal_value(self, data):
        # Если это файл (InMemoryUploadedFile), обрабатываем как ImageField
        if hasattr(data, 'read'):
            return super(serializers.ImageField, self).to_internal_value(data)
        # Если это base64-строка, обрабатываем как Base64ImageField
        return super().to_internal_value(data)


class UserRegistrationSerializer(UserCreateSerializer):
    """Serializer for user registration."""

    avatar = HybridImageField(required=False)

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


class UserProfileSerializer(UserSerializer):
    """Serializer for user profile."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = HybridImageField(required=False)

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
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription serializer."""

    class Meta:
        model = Subscription
        fields = ("user", "author")
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("user", "author"),
                message="Вы уже подписаны на этого автора.",
            )
        ]

    def validate(self, data):
        if data["user"] == data["author"]:
            raise serializers.ValidationError(
                "Невозможно подписаться на самого себя!"
            )
        return data


class AvatarSerializer(serializers.ModelSerializer):
    avatar = HybridImageField(required=False)

    class Meta:
        model = User
        fields = ("avatar",)


class SubscriptionListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='author.id',
        read_only=True
    )
    email = serializers.EmailField(
        source='author.email',
        read_only=True
    )
    username = serializers.CharField(
        source='author.username',
        read_only=True
    )
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True
    )
    avatar = HybridImageField(
        source='author.avatar',
        required=False
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'avatar',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        recipes_qs = obj.author.recipes.all()[:3]
        return ShortRecipeSerializer(
            recipes_qs, many=True,
            context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Текущий пароль неверен.')
        return value

    def validate_new_password(self, value):
        # Можно добавить дополнительные проверки пароля
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
