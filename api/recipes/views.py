"""
Views for the recipes API.
"""
from rest_framework import generics
from recipes.models import Recipe
from . import serializers

class RecipeListView(generics.ListCreateAPIView):
    """View for listing and creating recipes."""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating and deleting recipes."""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer 