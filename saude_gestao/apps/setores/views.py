from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Setor

# Setores que possuem app próprio.
# Adicione aqui qualquer novo setor com app dedicado: 'CODIGO': '/caminho/'
SETOR_APP_ROUTES = {
    'NSP': '/setor/nsp/',
    'NIR': '/setor/nir/',
}


@login_required
def dashboard(request):
    user = request.user
    setores_count = Setor.objects.filter(ativo=True).count()
    context = {
        'user': user,
        'setores_count': setores_count,
        'perfil': user.perfil,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def setor_detalhe(request, codigo):
    if codigo in SETOR_APP_ROUTES:
        return redirect(SETOR_APP_ROUTES[codigo])

    setor = get_object_or_404(Setor, codigo=codigo, ativo=True)
    user = request.user
    if not user.pode_ver_tudo:
        if user.setor != setor:
            permitidos = [user.setor] + user.setor.get_subordinados_recursivo() if user.setor else []
            if setor not in permitidos:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden('Acesso negado a este setor.')
    context = {'setor': setor, 'user': user}
    return render(request, 'setores/detalhe.html', context)


@login_required
def organograma(request):
    return render(request, 'setores/organograma.html', {'user': request.user})


@login_required
def setor_hub(request):
    """Landing page /setor/ — lista todos os apps de setor disponíveis."""
    apps = [
        {'codigo': k, 'url': v}
        for k, v in SETOR_APP_ROUTES.items()
    ]
    return render(request, 'setores/hub.html', {'user': request.user, 'apps': apps})
