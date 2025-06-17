from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self._handle_recipe_action(request, pk, Favorite, "favorite")

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self._handle_recipe_action(
            request, pk, ShoppingCart, "shopping_cart"
        )

    def _handle_recipe_action(self, request, pk, model, action_name):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == "POST":
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": f"Рецепт уже в {action_name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects.filter(recipe__shopping_cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )

        shopping_list = ["Список покупок:\n"]
        for ingredient in ingredients:
            shopping_list.append(
                f"{ingredient['ingredient__name']} - "
                f"{ingredient['amount']} "
                f"{ingredient['ingredient__measurement_unit']}\n"
            )

        response = HttpResponse(
            "".join(shopping_list), content_type="text/plain"
        )
        response["Content-Disposition"] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response
