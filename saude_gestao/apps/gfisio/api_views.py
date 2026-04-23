from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import AtendimentoFisio, StatusAtendimento, Especialidade, Modalidade
from .serializers import AtendimentoFisioSerializer


class AtendimentoListView(generics.ListCreateAPIView):
    serializer_class = AtendimentoFisioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = AtendimentoFisio.objects.select_related('setor_origem', 'profissional').order_by('-data_atendimento')
        p = self.request.query_params
        if p.get('status'):       qs = qs.filter(status=p['status'])
        if p.get('especialidade'): qs = qs.filter(especialidade=p['especialidade'])
        if p.get('modalidade'):   qs = qs.filter(modalidade=p['modalidade'])
        if p.get('setor'):        qs = qs.filter(setor_origem__codigo=p['setor'])
        return qs

    def perform_create(self, serializer):
        serializer.save(profissional=self.request.user)


class AtendimentoDetalheView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AtendimentoFisioSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AtendimentoFisio.objects.select_related('setor_origem', 'profissional')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def registrar_evolucao(request, pk):
    try:
        atd = AtendimentoFisio.objects.get(pk=pk)
    except AtendimentoFisio.DoesNotExist:
        return Response({'error': 'Atendimento não encontrado'}, status=404)

    atd.evolucao  = request.data.get('evolucao', atd.evolucao)
    atd.status    = request.data.get('status', StatusAtendimento.REALIZADO)
    atd.alta_fisioterapeutica = request.data.get('alta_fisioterapeutica', atd.alta_fisioterapeutica)
    atd.save()
    return Response(AtendimentoFisioSerializer(atd).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_gfisio(request):
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    qs = AtendimentoFisio.objects.all()
    qs_mes = qs.filter(data_atendimento__gte=inicio_mes)

    por_especialidade = list(
        qs_mes.values('especialidade').annotate(total=Count('id')).order_by('-total')
    )
    por_modalidade = list(
        qs_mes.values('modalidade').annotate(total=Count('id')).order_by('-total')
    )
    por_status = list(
        qs_mes.values('status').annotate(total=Count('id')).order_by('-total')
    )
    tendencia = list(
        qs.annotate(mes=TruncMonth('data_atendimento'))
        .values('mes').annotate(total=Count('id')).order_by('mes')
    )
    recentes = AtendimentoFisio.objects.select_related('setor_origem', 'profissional').order_by('-criado_em')[:8]

    return Response({
        'total_mes':      qs_mes.count(),
        'agendados':      qs.filter(status=StatusAtendimento.AGENDADO).count(),
        'realizados_mes': qs_mes.filter(status=StatusAtendimento.REALIZADO).count(),
        'altas_mes':      qs_mes.filter(alta_fisioterapeutica=True).count(),
        'por_especialidade': por_especialidade,
        'por_modalidade':    por_modalidade,
        'por_status':        por_status,
        'tendencia': [
            {'mes': d['mes'].strftime('%Y-%m') if d['mes'] else '', 'total': d['total']}
            for d in tendencia
        ],
        'recentes': AtendimentoFisioSerializer(recentes, many=True).data,
    })
