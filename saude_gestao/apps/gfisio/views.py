from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from apps.setores.models import Setor
from .models import AtendimentoFisio, Especialidade, Modalidade, StatusAtendimento


@login_required
def dashboard_gfisio(request):
    return render(request, 'gfisio/dashboard.html', {'user': request.user})


@login_required
def lista_atendimentos(request):
    return render(request, 'gfisio/atendimentos/lista.html', {
        'user': request.user,
        'especialidades': Especialidade.choices,
        'modalidades':    Modalidade.choices,
        'status_choices': StatusAtendimento.choices,
    })


@login_required
def novo_atendimento(request):
    setores = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    return render(request, 'gfisio/atendimentos/novo.html', {
        'user': request.user,
        'setores':        setores,
        'especialidades': Especialidade.choices,
        'modalidades':    Modalidade.choices,
    })


@login_required
def detalhe_atendimento(request, pk):
    atendimento = get_object_or_404(
        AtendimentoFisio.objects.select_related('setor_origem', 'profissional'),
        pk=pk
    )
    return render(request, 'gfisio/atendimentos/detalhe.html', {
        'user':        request.user,
        'atendimento': atendimento,
        'status_choices': StatusAtendimento.choices,
    })
