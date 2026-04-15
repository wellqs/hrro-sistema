from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from apps.setores.models import Setor
from .models import NotificacaoNSP, TipoIncidente, NivelDano, StatusNotificacao


@login_required
def dashboard_nsp(request):
    return render(request, 'nsp/dashboard.html', {'user': request.user})


@login_required
def lista_notificacoes(request):
    return render(request, 'nsp/notificacoes/lista.html', {
        'user': request.user,
        'tipos': TipoIncidente.choices,
        'danos': NivelDano.choices,
        'status_choices': StatusNotificacao.choices,
    })


@login_required
def nova_notificacao(request):
    setores = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    if not request.user.pode_ver_tudo and request.user.setor:
        setores = setores.filter(id=request.user.setor.id)
    return render(request, 'nsp/notificacoes/nova.html', {
        'user': request.user,
        'setores': setores,
        'tipos': TipoIncidente.choices,
        'danos': NivelDano.choices,
    })


@login_required
def detalhe_notificacao(request, pk):
    notificacao = get_object_or_404(
        NotificacaoNSP.objects.select_related('setor', 'notificado_por', 'analisado_por'),
        pk=pk
    )
    return render(request, 'nsp/notificacoes/detalhe.html', {
        'user': request.user,
        'notificacao': notificacao,
        'status_choices': StatusNotificacao.choices,
    })


@login_required
def metas_seguranca(request):
    return render(request, 'nsp/metas.html', {'user': request.user})
