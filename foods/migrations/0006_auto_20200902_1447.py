# Generated by Django 3.1 on 2020-09-02 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0005_auto_20200901_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='measure',
            field=models.CharField(default=None, max_length=300, null=True, verbose_name='measure'),
        ),
        migrations.AlterField(
            model_name='food',
            name='calorie',
            field=models.IntegerField(default=0, verbose_name='calorie'),
        ),
    ]
