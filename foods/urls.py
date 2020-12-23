from django.urls import path
from foods.views import AllRecipesView, RecipeDetailView, AddRecipeView, AddedRecipesView, EditRecipeView, \
    DeleteRecipeView, LikeRecipeView, UnlikeRecipeView, FavouriteRecipesView
from foods import views

urlpatterns = [
    path('addrecipe/', AddRecipeView.as_view(), name='addrecipe'),
    path('allrecipes/', AllRecipesView.as_view(), name="allrecipes"),
    path('detail/<int:recipe_id>', RecipeDetailView.as_view(), name='detail'),
    path('<int:recipe_id>/like', LikeRecipeView.as_view(), name='like'),
    path('<int:recipe_id>/unlike', UnlikeRecipeView.as_view(), name='unlike'),
    path('addedrecipes/', AddedRecipesView.as_view(), name='addedrecipes'),
    path('favouriterecipes/', FavouriteRecipesView.as_view(), name='favourite_recipes'),
    path('editrecipe/<int:recipe_id>/', EditRecipeView.as_view(), name='editrecipe'),
    path('deleterecipe/<int:recipe_id>/', DeleteRecipeView.as_view(), name='deleterecipe'),
]
