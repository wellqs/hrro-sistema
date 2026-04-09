from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import path
from .models import Setor


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
def alertas_view(request):
    return render(request, 'dashboard/alertas.html', {'user': request.user})


@login_required
def registro_view(request):
    setores = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    if not request.user.pode_ver_tudo and request.user.setor:
        setores = setores.filter(id=request.user.setor.id)
    return render(request, 'indicadores/registro.html', {
        'user': request.user,
        'setores': setores,
    })


urlpatterns_views = [
    path('', dashboard, name='dashboard'),
    path('setor/<str:codigo>/', setor_detalhe, name='setor-detalhe'),
    path('organograma/', organograma, name='organograma'),
    path('alertas/', alertas_view, name='alertas'),
    path('registro/', registro_view, name='registro'),
]
