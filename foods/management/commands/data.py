import csv
from decimal import Decimal

from django.core.management import BaseCommand
from foods.models import Food


class Command(BaseCommand):

    def handle(self, *args, **options):
        food_portion = {}
        food_cal = {}
        food_carb = {}
        food_protein = {}
        food_fat = {}

        with open('foods/management/commands/Total_Kcal.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                food_portion[row[0]] = row[1]
                food_cal[row[0]] = row[2]

        with open('foods/management/commands/protein.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:

                if food_portion.get(row[0]) is None:
                    food_portion[row[0]] = row[1]

                food_protein[row[0]] = row[2]

        print(len(food_portion.items()))

        with open('foods/management/commands/carbohydrate.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:

                if food_portion.get(row[0]) is None:
                    food_portion[row[0]] = row[1]

                food_carb[row[0]] = row[2]

        print(len(food_carb.items()))

        with open('foods/management/commands/sat_fat.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:

                if food_portion.get(row[0]) is None:
                    food_portion[row[0]] = row[1]

                food_fat[row[0]] = row[2]

        print(len(food_portion.items()))

        for food_name in food_portion.keys():
            new_food = Food()
            new_food.name = food_name
            new_food.measure = food_portion.get(food_name)

            if food_cal.get(food_name) is not None:
                new_food.calorie = int(food_cal.get(food_name))

            if food_carb.get(food_name) is not None:
                new_food.carbohydrate = Decimal(food_carb.get(food_name))

            if food_protein.get(food_name) is not None:
                new_food.protein = Decimal(food_protein.get(food_name))

            if food_fat.get(food_name) is not None:
                new_food.fats = Decimal(food_fat.get(food_name))

            new_food.save()



