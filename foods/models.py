from django.db import models
from django.utils import timezone
from accounts.models import User, UserAppearance


class Food(models.Model):
    name = models.CharField(max_length=300)
    calorie = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    measure = models.CharField(max_length=300, verbose_name="measure", null=True, default=None)

    def __str__(self):
        return str(self.name)


class DailyFood(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="user")
    date = models.DateTimeField(default=timezone.now, verbose_name='date')
    eatenfood = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='eatenfood', null=True, default=None)
    portion = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="portion", default=1)
    calorie = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbohydrate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.user.username)


class Recipe(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="user")
    date = models.DateTimeField(default=timezone.now, verbose_name='date')
    title = models.CharField(verbose_name="title", max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='images/')
    likes = models.IntegerField(default=0)

    def summary(self):
        return self.text[:100]

    def date_pretty(self):
        return self.date.strftime('%b %e %Y')

    def __str__(self):
        return self.title


class Like(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="like", null=True, blank=True)
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="user")
