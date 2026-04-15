from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import SolicitacaoNIR, TipoSolicitacao, Prioridade, StatusSolicitacao, Clinica, Leito, StatusLeito
from .serializers import SolicitacaoNIRSerializer


class SolicitacaoListView(generics.ListCreateAPIView):
    serializer_class = SolicitacaoNIRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = SolicitacaoNIR.objects.select_related('setor', 'solicitado_por').order_by('-data_solicitacao')
        if not user.pode_ver_tudo and user.setor:
            qs = qs.filter(setor=user.setor)

        tipo       = self.request.query_params.get('tipo')
        prioridade = self.request.query_params.get('prioridade')
        status     = self.request.query_params.get('status')
        setor      = self.request.query_params.get('setor')
        if tipo:       qs = qs.filter(tipo=tipo)
        if prioridade: qs = qs.filter(prioridade=prioridade)
        if status:     qs = qs.filter(status=status)
        if setor:      qs = qs.filter(setor__codigo=setor)
        return qs

    def perform_create(self, serializer):
        serializer.save(solicitado_por=self.request.user)


class SolicitacaoDetalheView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SolicitacaoNIRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SolicitacaoNIR.objects.select_related('setor', 'solicitado_por', 'regulado_por')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def regular_solicitacao(request, pk):
    try:
        sol = SolicitacaoNIR.objects.get(pk=pk)
    except SolicitacaoNIR.DoesNotExist:
        return Response({'error': 'Solicitação não encontrada'}, status=404)

    novo_status = request.data.get('status', StatusSolicitacao.EM_REGULACAO)
    observacoes = request.data.get('observacoes', '')

    sol.status = novo_status
    sol.regulado_por = request.user
    if novo_status in (StatusSolicitacao.AUTORIZADO, StatusSolicitacao.NEGADO, StatusSolicitacao.CONCLUIDO):
        sol.data_regulacao = timezone.now().date()
    if observacoes:
        sol.observacoes = observacoes
    sol.save()
    return Response(SolicitacaoNIRSerializer(sol).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_nir(request):
    user = request.user
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    qs = SolicitacaoNIR.objects.all()
    if not user.pode_ver_tudo and user.setor:
        qs = qs.filter(setor=user.setor)

    qs_mes = qs.filter(data_solicitacao__gte=inicio_mes)

    por_tipo = list(
        qs_mes.values('tipo').annotate(total=Count('id')).order_by('-total')
    )
    por_prioridade = list(
        qs.filter(status__in=[StatusSolicitacao.SOLICITADO, StatusSolicitacao.EM_REGULACAO])
        .values('prioridade').annotate(total=Count('id')).order_by('-total')
    )
    por_status = list(
        qs_mes.values('status').annotate(total=Count('id')).order_by('-total')
    )
    tendencia = list(
        qs.annotate(mes=TruncMonth('data_solicitacao'))
        .values('mes').annotate(total=Count('id')).order_by('mes')
    )
    recentes = SolicitacaoNIR.objects.select_related('setor', 'solicitado_por').order_by('-criado_em')
    if not user.pode_ver_tudo and user.setor:
        recentes = recentes.filter(setor=user.setor)

    emergencias_abertas = qs.filter(
        prioridade=Prioridade.EMERGENCIA,
        status__in=[StatusSolicitacao.SOLICITADO, StatusSolicitacao.EM_REGULACAO]
    ).count()

    return Response({
        'total_mes':          qs_mes.count(),
        'solicitadas':        qs.filter(status=StatusSolicitacao.SOLICITADO).count(),
        'em_regulacao':       qs.filter(status=StatusSolicitacao.EM_REGULACAO).count(),
        'emergencias_abertas': emergencias_abertas,
        'por_tipo':           por_tipo,
        'por_prioridade':     por_prioridade,
        'por_status':         por_status,
        'tendencia': [
            {'mes': d['mes'].strftime('%Y-%m') if d['mes'] else '', 'total': d['total']}
            for d in tendencia
        ],
        'recentes': SolicitacaoNIRSerializer(recentes[:8], many=True).data,
    })


# ─── Painel de Leitos ────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def painel_leitos(request):
    clinicas = Clinica.objects.prefetch_related('leitos').order_by('ordem')
    dados = []
    total_livre = total_ocupado = total_reservado = total_outros = 0

    for c in clinicas:
        leitos = list(c.leitos.all())
        livre     = sum(1 for l in leitos if l.status == StatusLeito.LIVRE)
        ocupado   = sum(1 for l in leitos if l.status == StatusLeito.OCUPADO)
        reservado = sum(1 for l in leitos if l.status == StatusLeito.RESERVADO)
        outros    = len(leitos) - livre - ocupado - reservado

        total_livre     += livre
        total_ocupado   += ocupado
        total_reservado += reservado
        total_outros    += outros

        dados.append({
            'id':         c.id,
            'nome':       c.nome,
            'cor':        c.cor,
            'capacidade': c.capacidade,
            'resumo': {'livre': livre, 'ocupado': ocupado, 'reservado': reservado, 'outros': outros},
            'leitos': [
                {
                    'id':            l.id,
                    'numero':        l.numero,
                    'status':        l.status,
                    'paciente_nome': l.paciente_nome,
                    'observacao':    l.observacao,
                    'atualizado_em': l.atualizado_em.strftime('%d/%m %H:%M') if l.atualizado_em else '',
                }
                for l in leitos
            ],
        })

    total = total_livre + total_ocupado + total_reservado + total_outros
    return Response({
        'totais': {
            'geral':     total,
            'livre':     total_livre,
            'ocupado':   total_ocupado,
            'reservado': total_reservado,
            'outros':    total_outros,
        },
        'clinicas': dados,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def atualizar_leito(request, pk):
    try:
        leito = Leito.objects.get(pk=pk)
    except Leito.DoesNotExist:
        return Response({'error': 'Leito não encontrado'}, status=404)

    status        = request.data.get('status')
    paciente_nome = request.data.get('paciente_nome', leito.paciente_nome)
    observacao    = request.data.get('observacao', leito.observacao)

    if status not in StatusLeito.values:
        return Response({'error': 'Status inválido'}, status=400)

    leito.status        = status
    leito.paciente_nome = paciente_nome if status == StatusLeito.OCUPADO else ''
    leito.observacao    = observacao
    leito.atualizado_por = request.user
    leito.save()

    return Response({
        'id':            leito.id,
        'numero':        leito.numero,
        'status':        leito.status,
        'paciente_nome': leito.paciente_nome,
        'observacao':    leito.observacao,
        'atualizado_em': leito.atualizado_em.strftime('%d/%m %H:%M'),
    })
