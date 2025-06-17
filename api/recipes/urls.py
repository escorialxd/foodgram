"""
URL configuration for the recipes API.
"""
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
] 