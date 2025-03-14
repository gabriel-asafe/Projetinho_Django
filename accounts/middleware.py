# accounts/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/login/',         
            '/logout/',      
            '/admin/',        
            '/accounts/login/',  
            '/accounts/register/'
        ]

    def __call__(self, request):

        print(f"Middleware: Usuário autenticado: {request.user.is_authenticated}, Caminho: {request.path}, Isento: {request.path in self.exempt_urls}")
        
        if not request.user.is_authenticated:
            if request.path not in self.exempt_urls:
                messages.warning(request, 'É necessário fazer login para acessar essa página.')
                return redirect(f"{reverse('accounts:login')}?next={request.path}")
        
        response = self.get_response(request)
        return response