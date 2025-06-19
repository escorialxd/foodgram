from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

MAX_NAME_LENGTH = 200
MAX_COLOR_LENGTH = 7
MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        "Название",
        max_length=MAX_NAME_LENGTH,
        unique=True,
    )
    color = models.CharField(
        "Цвет в HEX",
        max_length=MAX_COLOR_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        "Slug",
        max_length=MAX_NAME_LENGTH,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        "Название",
        max_length=MAX_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        "Единица измерения",
        max_length=MAX_NAME_LENGTH,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]
        constraints = [
            UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )

    name = models.CharField(
        "Название",
        max_length=MAX_NAME_LENGTH,
    )
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
    )
    text = models.TextField(
        "Описание",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления (в минутах)",
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f"Минимальное время приготовления - {MIN_COOKING_TIME} минута"
            )
        ],
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингредиента."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name="Ингредиент",
    )

    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=[MinValueValidator(
            MIN_INGREDIENT_AMOUNT,
            f"Минимальное количество - {MIN_INGREDIENT_AMOUNT}"
        )],
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            UniqueConstraint(fields=["user", "recipe"], name="unique_favorite")
        ]


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart"
            )
        ]
