"""
Serializers for the recipes API.
"""
from rest_framework import serializers
from recipes.models import Recipe, Ingredient, Tag

class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'text', 'cooking_time', 'ingredients', 'tags'] 