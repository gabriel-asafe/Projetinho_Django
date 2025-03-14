from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from accounts.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def project_list(request):
    projects = Project.objects.filter(membros=request.user)
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.dono = request.user
            project.save()
            project.membros.add(request.user) 
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, dono=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form})

@login_required(login_url='/login/')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, dono=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('projects:project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required(login_url='/login/')
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, membros=request.user)
    tasks = project.tarefas.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})

@login_required(login_url='/accounts/login/')
def project_manage_members(request, pk):
    project = get_object_or_404(Project, pk=pk, dono=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            email = request.POST.get('email')
            try:
                user_to_add = User.objects.get(email=email)
                if user_to_add not in project.membros.all():
                    project.membros.add(user_to_add)
                    messages.success(request, f'{user_to_add.first_name or user_to_add.email} adicionado ao projeto.', extra_tags='members')
                else:
                    messages.warning(request, f'{user_to_add.first_name or user_to_add.email} já é membro.', extra_tags='members')
            except User.DoesNotExist:
                messages.error(request, f'Usuário com e-mail {email} não encontrado.', extra_tags='members')
        elif action == 'remove':
            user_id = request.POST.get('user_id')
            user_to_remove = get_object_or_404(User, id=user_id)
            if user_to_remove in project.membros.all() and user_to_remove != project.dono:
                project.membros.remove(user_to_remove)
                messages.success(request, f'{user_to_remove.first_name or user_to_remove.email} removido do projeto.', extra_tags='members')
            else:
                messages.warning(request, 'Não é possível remover este usuário.', extra_tags='members')
        return redirect('projects:project_manage_members', pk=project.pk)

    return render(request, 'projects/project_manage_members.html', {
        'project': project,
        'members': project.membros.all(),
    })