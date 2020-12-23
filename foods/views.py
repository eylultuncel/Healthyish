from decimal import Decimal
import django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from exercise.models import DailyExercise
from .models import DailyFood, Recipe, Food, Like
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.models import UserAppearance
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class HomeView(View):
    def get(self, request):
        all_recipes = Recipe.objects.all().order_by('-id')[:6]
        return render(request, 'index.html', {'all_recipes': all_recipes})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_appearance = UserAppearance.objects.get(user=user)
        eaten_foods = []
        exercises_done = []
        total_calorie = 0
        total_carb = 0
        total_protein = 0
        total_fat = 0
        today_foods = DailyFood.objects.filter(
            date__gte=django.utils.timezone.now().replace(hour=0, minute=0, second=0),
            user=user)
        today_exercise = DailyExercise.objects.filter(
            date__gte=django.utils.timezone.now().replace(hour=0, minute=0, second=0),
            user=user)
        for x in today_foods:
            eaten_foods.append(x)
            total_calorie += Decimal(x.eatenfood.calorie * x.portion)
            total_carb += x.eatenfood.carbohydrate * x.portion
            total_protein += x.eatenfood.protein * x.portion
            total_fat += x.eatenfood.fats * x.portion
        total_exercise_cal = 0
        total_duration = 0
        for x in today_exercise:
            exercises_done.append(x)
            total_exercise_cal += x.calorie
            total_duration += x.duration

        return render(request, 'profile.html',
                      {'foods': eaten_foods,
                       'user': user,
                       'total_calorie': total_calorie,
                       'bmi': user_appearance.bmi,
                       'daily_calorie': user_appearance.dailycalorie,
                       'total_carb': total_carb,
                       'total_protein': total_protein,
                       'total_fat': total_fat,
                       'exercises_done': exercises_done,
                       'total_exercise_cal': total_exercise_cal,
                       'total_duration': total_duration,
                       })


class FoodsView(LoginRequiredMixin, View):
    def post(self, request):
        today_food = DailyFood()
        today_food.eatenfood = Food.objects.get(name=request.POST['foods'])
        today_food.portion = Decimal(request.POST['portion'])
        today_food.user = request.user
        today_food.calorie = int(Decimal(today_food.eatenfood.calorie) * Decimal(today_food.portion))
        today_food.carbohydrate = Decimal(today_food.eatenfood.carbohydrate) * Decimal(today_food.portion)
        today_food.protein = Decimal(today_food.eatenfood.protein) * Decimal(today_food.portion)
        today_food.fats = Decimal(today_food.eatenfood.fats) * Decimal(today_food.portion)
        today_food.save()
        return redirect('profile')

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            all_foods = Food.objects.all()
            eaten_foods = []
            today_foods = DailyFood.objects.filter(
                date__gte=django.utils.timezone.now().replace(hour=0, minute=0, second=0),
                user=user)
            for x in today_foods:
                eaten_foods.append(x)
            return render(request, 'food.html', {'eaten_foods': eaten_foods,
                                                 'all_foods': all_foods})
        else:
            return render(request, 'login.html')


class AllRecipesView(View):
    def post(self, request):
        search = request.POST['search']
        recipe_list = Recipe.objects.filter(Q(title__icontains=search) | Q(text__icontains=search))
        paginator = Paginator(recipe_list, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'allrecipes.html', {'page_obj': page_obj})

    def get(self, request):
        recipe_list = Recipe.objects.all()
        paginator = Paginator(recipe_list, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'allrecipes.html', {'page_obj': page_obj})


class AddRecipeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            if request.POST['title'] and request.POST['text'] and request.FILES['image']:
                recipe = Recipe()
                recipe.title = request.POST['title']
                recipe.text = request.POST['text']
                recipe.image = request.FILES['image']
                recipe.date = timezone.datetime.now()
                recipe.user = request.user
                recipe.save()
                return redirect('allrecipes')
            else:
                error = "Your form is not valid, please try again."
                return render(request, 'addrecipe.html', {'error': error})
        except MultiValueDictKeyError:
            error = "Your form is not valid, please try again."
            return render(request, 'addrecipe.html', {'error': error})

    def get(self, request):
        return render(request, 'addrecipe.html')


class RecipeDetailView(View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        all_recipes = Recipe.objects.values()
        data = pd.DataFrame(all_recipes)
        final_data = data[["title", "text"]]
        final_data = final_data.set_index('title')

        final_data['text'].dropna(inplace=True)
        stop_words = set(stopwords.words('english'))

        for title, text in final_data.iterrows():
            text = [entry.lower() for entry in text]
            text = [nltk.word_tokenize(txt) for txt in text]
            for recipes in text:
                recipes = [word for word in recipes if word.isalpha()]
                recipes = [w for w in recipes if not w in stop_words]
                porter = PorterStemmer()
                recipes = [porter.stem(word) for word in recipes]
                text[0] = recipes
            text = '\n'.join(' '.join(elems) for elems in text)
            final_data.loc[title, "text_processed"] = text

        print(final_data.head(10))

        tfidf_vec = TfidfVectorizer()
        tfidf_recipe_id = tfidf_vec.fit_transform((final_data["text_processed"]))

        cos_sim = cosine_similarity(tfidf_recipe_id, tfidf_recipe_id)

        indices = pd.Series(final_data.index)

        recommended_recipes = []
        index = indices[indices == recipe.title ].index[0]
        similarity_scores = pd.Series(cos_sim[index]).sort_values(ascending=False)
        top_9_recipe = list(similarity_scores.iloc[1:10].index)
        for i in top_9_recipe:
            recommended_recipes.append(list(final_data.index)[i])

        recommendations = []
        for x in recommended_recipes:
            rcp = Recipe.objects.get(title=x)
            recommendations.append(rcp)

        if not request.user.is_anonymous:
            if Like.objects.filter(recipe=recipe, user=request.user).count() != 0:
                return render(request, 'recipedetail.html', {'recipe': recipe,
                                                             'is_liked': True,
                                                             'recommendations': recommendations})
            else:
                return render(request, 'recipedetail.html', {'recipe': recipe,
                                                             'recommendations': recommendations})
        else:
            return render(request, 'recipedetail.html', {'recipe': recipe,
                                                         'recommendations': recommendations})


class AddedRecipesView(LoginRequiredMixin, View):
    def get(self, request):
        added_recipes = Recipe.objects.filter(user=request.user)
        paginator = Paginator(added_recipes, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'addedrecipes.html', {'page_obj': page_obj})


class FavouriteRecipesView(LoginRequiredMixin, View):
    def get(self, request):
        liked_recipes = Like.objects.filter(user=request.user)
        favourite_recipes = []
        for rcp in liked_recipes:
            favourite_recipes.append(rcp.recipe)
        paginator = Paginator(favourite_recipes, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'favourite_recipes.html', {'page_obj': page_obj})


class EditRecipeView(LoginRequiredMixin, View):
    def post(self, request, recipe_id):
        if request.POST['title'] and request.POST['text']:
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            recipe.date = timezone.datetime.now()
            recipe.user = request.user
            recipe.title = request.POST['title']
            recipe.text = request.POST['text']
            recipe.image = request.FILES.get('image',recipe.image)
            recipe.save()
            return redirect('addedrecipes')
        else:
            error = "Your form is not valid, please try again."
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            return render(request, 'editrecipe.html', {'error': error,
                                                       'recipe': recipe})

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user == recipe.user:
            return render(request, 'editrecipe.html', {'recipe': recipe})
        else:
            return render(request, 'login.html')


class DeleteRecipeView(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        deleted_recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user == deleted_recipe.user:
            deleted_recipe.delete()
            return redirect('addedrecipes')
        else:
            return render(request, 'login.html')


class BMIView(View):
    def get(self, request):
        return render(request, 'bmi.html')


class DailyCalorieView(View):
    def get(self, request):
        return render(request, 'dailycalorie.html')


class DeleteFoodView(LoginRequiredMixin, View):
    def get(self, request, food_id):
        deleted_food = get_object_or_404(DailyFood, pk=food_id)
        if deleted_food.user == request.user:
            deleted_food.delete()
            return redirect('profile')
        else:
            return render(request, 'login.html')


class LikeRecipeView(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        if Like.objects.filter(recipe=recipe, user=request.user).count() != 0:
            return redirect('/recipes/detail/' + str(recipe.id))
        else:
            recipe.likes += 1
            like = Like()
            like.user = request.user
            like.recipe = recipe
            like.save()
            recipe.save()
        data = {
            'like': recipe.likes
        }
        return JsonResponse(data)


class UnlikeRecipeView(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.likes -= 1
        recipe.save()
        like = Like.objects.filter(user=request.user, recipe=recipe)
        like.delete()
        data = {
            'like': recipe.likes
        }
        return JsonResponse(data)
