# task_manager/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'base.html')