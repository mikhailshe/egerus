from django.db import models

class Task(models.Model):
    task_type = models.IntegerField(choices=[(i, f'Задание {i}') for i in range(1, 27)])
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Задание {self.task_type}"