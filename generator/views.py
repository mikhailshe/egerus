from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
import random
from django.shortcuts import render
from .models import Task

def index(request):
    return render(request, 'generator/index.html')

def generate_variant(request):
    variant = []
    for task_type in range(1, 27):
        tasks = Task.objects.filter(task_type=task_type)
        if tasks.exists():
            variant.append(random.choice(tasks))
    request.session['variant_ids'] = [t.id for t in variant]
    return render(request, 'generator/variant.html', {'variant': variant})

def check_variant(request):
    variant_ids = request.session.get('variant_ids', [])
    results = []

    for i, task_id in enumerate(variant_ids, 1):
        user_answer = request.POST.get(f'answer_{i}', '').strip()
        try:
            task = Task.objects.get(id=task_id)
            correct = task.correct_answer.strip().lower() == user_answer.lower()
            results.append({
                'task': task,
                'user_answer': user_answer,
                'is_correct': correct,
            })
        except Task.DoesNotExist:
            continue

    return render(request, 'generator/check_results.html', {'results': results})

def run_parser_view(request):
    try:
        call_command('run_parser')
        return HttpResponse("Парсинг завершён!")
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")

def index(request):
    return render(request, 'generator/index.html')
