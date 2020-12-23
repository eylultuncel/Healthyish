from django.urls import path
from exercise.views import ExercisesView, DeleteExerciseView
from foods import views

urlpatterns = [
    path('addexercise/', ExercisesView.as_view(), name='exercises'),
    path('delete_exercise/<int:exercise_id>/', DeleteExerciseView.as_view(), name='delete_exercise'),
    ]
