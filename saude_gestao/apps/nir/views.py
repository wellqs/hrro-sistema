from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from apps.setores.models import Setor
from .models import SolicitacaoNIR, TipoSolicitacao, Prioridade, StatusSolicitacao, StatusLeito


def _nir_context(request, active_tab='dashboard', **extra):
    setor = get_object_or_404(
        Setor.objects.select_related('parent'),
        codigo='NIR',
        ativo=True,
    )
    return {
        'user': request.user,
        'nir_setor': setor,
        'nir_active_tab': active_tab,
        **extra,
    }


@login_required
def dashboard_nir(request):
    return render(request, 'nir/dashboard.html', _nir_context(request, 'dashboard'))


@login_required
def lista_solicitacoes(request):
    return render(request, 'nir/solicitacoes/lista.html', _nir_context(
        request,
        'solicitacoes',
        tipos=TipoSolicitacao.choices,
        prioridades=Prioridade.choices,
        status_choices=StatusSolicitacao.choices,
    ))


@login_required
def nova_solicitacao(request):
    setores = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    if not request.user.pode_ver_tudo and request.user.setor:
        setores = setores.filter(id=request.user.setor.id)
    return render(request, 'nir/solicitacoes/nova.html', _nir_context(
        request,
        'solicitacoes',
        setores=setores,
        tipos=TipoSolicitacao.choices,
        prioridades=Prioridade.choices,
    ))


@login_required
def detalhe_solicitacao(request, pk):
    solicitacao = get_object_or_404(
        SolicitacaoNIR.objects.select_related('setor', 'solicitado_por', 'regulado_por'),
        pk=pk
    )
    return render(request, 'nir/solicitacoes/detalhe.html', _nir_context(
        request,
        'solicitacoes',
        solicitacao=solicitacao,
        status_choices=StatusSolicitacao.choices,
    ))


@login_required
def painel_leitos(request):
    return render(request, 'nir/painel_leitos.html', _nir_context(
        request,
        'painel',
        status_choices=StatusLeito.choices,
    ))
