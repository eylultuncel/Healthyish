from django.db import models
from django.utils import timezone
from accounts.models import User, UserAppearance


class Exercise(models.Model):
    name = models.CharField(max_length=400)
    type = models.CharField(max_length=400)
    met = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name)


class DailyExercise(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="user")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="exercise")
    date = models.DateTimeField(default=timezone.now, verbose_name='date')
    duration = models.IntegerField(verbose_name='duration')
    calorie = models.IntegerField(verbose_name='calorie')

    def __str__(self):
        return str(self.user.username)
