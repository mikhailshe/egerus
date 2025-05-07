import csv
from django.core.management.base import BaseCommand
from generator.models import Task

class Command(BaseCommand):
    help = 'Импортирует задания из CSV, созданного парсером'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Путь к CSV-файлу')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                Task.objects.create(
                    task_type=int(row['task_type']),
                    question_text=row['question_text'],
                    correct_answer=row['correct_answer'],
                    explanation=row.get('explanation', '')
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Импортировано заданий: {count}'))