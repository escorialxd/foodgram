from rest_framework import serializers
from recipes.models import Recipe
from recipes.fields import Base64ImageField


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time') 