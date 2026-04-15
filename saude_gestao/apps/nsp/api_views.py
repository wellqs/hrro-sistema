from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import NotificacaoNSP, TipoIncidente, NivelDano, StatusNotificacao, MetaSeguranca
from .serializers import NotificacaoNSPSerializer


class NotificacaoListView(generics.ListCreateAPIView):
    serializer_class = NotificacaoNSPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = NotificacaoNSP.objects.select_related('setor', 'notificado_por').order_by('-data_ocorrencia')
        if not user.pode_ver_tudo and user.setor:
            qs = qs.filter(setor=user.setor)
        tipo = self.request.query_params.get('tipo')
        dano = self.request.query_params.get('dano')
        status = self.request.query_params.get('status')
        setor = self.request.query_params.get('setor')
        if tipo:
            qs = qs.filter(tipo=tipo)
        if dano:
            qs = qs.filter(dano=dano)
        if status:
            qs = qs.filter(status=status)
        if setor:
            qs = qs.filter(setor__codigo=setor)
        return qs


class NotificacaoDetalheView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificacaoNSPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NotificacaoNSP.objects.select_related('setor', 'notificado_por', 'analisado_por')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def analisar_notificacao(request, pk):
    try:
        notif = NotificacaoNSP.objects.get(pk=pk)
    except NotificacaoNSP.DoesNotExist:
        return Response({'error': 'Notificação não encontrada'}, status=404)
    novo_status = request.data.get('status', StatusNotificacao.EM_ANALISE)
    plano = request.data.get('plano_acao', '')
    notif.status = novo_status
    notif.analisado_por = request.user
    if plano:
        notif.plano_acao = plano
    notif.save()
    return Response(NotificacaoNSPSerializer(notif).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_nsp(request):
    user = request.user
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    qs = NotificacaoNSP.objects.all()
    if not user.pode_ver_tudo and user.setor:
        qs = qs.filter(setor=user.setor)

    qs_mes = qs.filter(data_ocorrencia__gte=inicio_mes)

    por_tipo = list(
        qs_mes.values('tipo').annotate(total=Count('id')).order_by('-total')
    )
    por_dano = list(
        qs_mes.values('dano').annotate(total=Count('id')).order_by('-total')
    )
    por_meta = list(
        qs.filter(status=StatusNotificacao.ABERTA)
        .values('meta_relacionada').annotate(total=Count('id')).order_by('-total')
    )
    tendencia = list(
        qs.annotate(mes=TruncMonth('data_ocorrencia'))
        .values('mes').annotate(total=Count('id')).order_by('mes')
    )
    recentes = NotificacaoNSP.objects.select_related('setor', 'notificado_por').order_by('-criado_em')
    if not user.pode_ver_tudo and user.setor:
        recentes = recentes.filter(setor=user.setor)

    return Response({
        'total_mes': qs_mes.count(),
        'abertas': qs.filter(status=StatusNotificacao.ABERTA).count(),
        'em_analise': qs.filter(status=StatusNotificacao.EM_ANALISE).count(),
        'graves_mes': qs_mes.filter(dano__in=[NivelDano.GRAVE, NivelDano.OBITO]).count(),
        'por_tipo': por_tipo,
        'por_dano': por_dano,
        'por_meta': por_meta,
        'tendencia': [
            {'mes': d['mes'].strftime('%Y-%m') if d['mes'] else '', 'total': d['total']}
            for d in tendencia
        ],
        'recentes': NotificacaoNSPSerializer(recentes[:8], many=True).data,
    })
