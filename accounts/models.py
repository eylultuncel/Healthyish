from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sex(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)


class UserAppearance(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="user")
    weight = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="weight")
    height = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="height")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="age")
    bmi = models.IntegerField(verbose_name="bmi")
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE, verbose_name='gender')
    dailycalorie = models.IntegerField(verbose_name='dailycalorie')

    def __str__(self):
        return str(self.user.username)




