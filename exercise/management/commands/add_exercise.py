import csv
from decimal import Decimal

from django.core.management import BaseCommand
from exercise.models import Exercise


class Command(BaseCommand):

    def handle(self, *args, **options):

        exercise_type = {}
        exercise_met = {}

        count = 1
        with open('exercise/management/commands/exercise.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                if exercise_type.get(row[1]) is None:
                    exercise_type[row[1]] = row[0]
                    exercise_met[row[1]] = row[2]

        for exercise in exercise_type.keys():
            new_exercise = Exercise()
            new_exercise.name = exercise
            new_exercise.type = exercise_type.get(exercise)
            new_exercise.met = Decimal(exercise_met.get(exercise))
            new_exercise.save()
