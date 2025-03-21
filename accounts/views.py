
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:task_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"Login bem-sucedido. Usuário: {user}, Session ID: {request.session.session_key}")
            next_url = request.GET.get('next', 'tasks:task_list')
            messages.success(request, 'Login realizado com sucesso!')
            return redirect(next_url)
        else:
            print(f"Erro de autenticação: {form.errors}")
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    print(f"Logout chamado. Usuário: {request.user}, Session ID: {request.session.session_key}")
    logout(request)
    messages.info(request, 'Você saiu com sucesso.')
    return redirect('accounts:login')
    
def register_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:task_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cadastro realizado com sucesso para {username}! Faça login para continuar.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})