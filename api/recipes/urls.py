from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet, basename='tags')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/favorite/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('recipes/download_shopping_cart/', views.DownloadShoppingCartView.as_view(), name='download-shopping-cart'),
]
