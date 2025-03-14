from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
@login_required(login_url='/login/')
def task_list(request):
    tasks = Task.objects.filter(projeto__membros=request.user).distinct()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required(login_url='/login/')
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.usuario_atribuido = request.user
            task.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(initial={'usuario_atribuido': request.user})
        form.fields['projeto'].queryset = request.user.projetos_participados.all()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required(login_url='/login/')
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, projeto__membros=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task, initial={'usuario_atribuido': request.user})
        form.fields['projeto'].queryset = request.user.projetos_participados.all()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required(login_url='/login/')
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, projeto__membros=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required(login_url='/login/')
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, projeto__membros=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})