# Generated by Django 3.1 on 2020-09-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0010_auto_20200909_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyfood',
            name='calorie',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]