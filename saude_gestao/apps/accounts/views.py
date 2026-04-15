from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user and user.ativo:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'accounts/login.html')


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('login')
