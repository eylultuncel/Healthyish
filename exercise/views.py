from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .models import Exercise, DailyExercise
from accounts.models import UserAppearance
import django
from django.utils import timezone


class ExercisesView(LoginRequiredMixin, View):
    def post(self, request):
        today_exercise = DailyExercise()
        today_exercise.user = request.user
        today_exercise.exercise = Exercise.objects.get(name=request.POST['exercises'])
        today_exercise.duration = request.POST['duration']
        users_weight = UserAppearance.objects.get(user=request.user).weight
        today_exercise.calorie = \
            int(int(today_exercise.duration) * (int(today_exercise.exercise.met * Decimal(3.5)) * users_weight) / 200)
        today_exercise.save()
        return redirect('profile')

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            all_exercises = Exercise.objects.all()
            exercises_done = []
            today_exercise = DailyExercise.objects.filter(
                date__gte=django.utils.timezone.now().replace(hour=0, minute=0, second=0),
                user=user)
            for x in today_exercise:
                exercises_done.append(x)
            return render(request, 'exercise.html', {'exercises_done': exercises_done, 'all_exercises': all_exercises})
        else:
            return render(request, 'login.html')


class DeleteExerciseView(LoginRequiredMixin, View):
    def get(self, request, exercise_id):
        deleted_exercise = get_object_or_404(DailyExercise, pk=exercise_id)
        if deleted_exercise.user == request.user:
            deleted_exercise.delete()
            return redirect('profile')
        else:
            return render(request, 'login.html')
