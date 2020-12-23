# Generated by Django 3.1 on 2020-08-25 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('calorie', models.IntegerField(verbose_name='calorie')),
                ('carbohydrate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('fats', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('protein', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('portion', models.IntegerField(default=1, verbose_name='portion')),
            ],
        ),
        migrations.CreateModel(
            name='DailyFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('eatenfood', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='foods.food', verbose_name='eatenfood')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]