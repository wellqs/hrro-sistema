from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Avg, Max, Min, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from .models import Indicador, Registro
from .serializers import IndicadorSerializer, RegistroSerializer
from apps.setores.models import Setor


class IndicadorListView(generics.ListCreateAPIView):
    serializer_class = IndicadorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Indicador.objects.filter(ativo=True).select_related('setor')
        setor_codigo = self.request.query_params.get('setor')
        if setor_codigo:
            qs = qs.filter(setor__codigo=setor_codigo)
        elif not user.pode_ver_tudo and user.setor:
            qs = qs.filter(setor=user.setor)
        return qs


class RegistroListView(generics.ListCreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Registro.objects.select_related('indicador__setor', 'usuario').order_by('-data_referencia')
        setor = self.request.query_params.get('setor')
        indicador = self.request.query_params.get('indicador')
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        status_filter = self.request.query_params.get('status')

        if setor:
            qs = qs.filter(indicador__setor__codigo=setor)
        elif not user.pode_ver_tudo and user.setor:
            qs = qs.filter(indicador__setor=user.setor)
        if indicador:
            qs = qs.filter(indicador_id=indicador)
        if data_inicio:
            qs = qs.filter(data_referencia__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data_referencia__lte=data_fim)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class RegistroDetalheView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registro.objects.select_related('indicador__setor', 'usuario')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def grafico_setor(request, codigo):
    try:
        setor = Setor.objects.get(codigo=codigo)
    except Setor.DoesNotExist:
        return Response({'error': 'Setor não encontrado'}, status=404)

    tipo = request.query_params.get('tipo')
    qs = Registro.objects.filter(indicador__setor=setor)
    if tipo:
        qs = qs.filter(indicador__tipo=tipo)

    dados = (
        qs.annotate(mes=TruncMonth('data_referencia'))
        .values('mes', 'indicador__tipo')
        .annotate(total=Sum('valor'), media=Avg('valor'), maximo=Max('valor'), minimo=Min('valor'))
        .order_by('mes')
    )

    resultado = []
    for d in dados:
        resultado.append({
            'mes': d['mes'].strftime('%Y-%m') if d['mes'] else '',
            'tipo': d['indicador__tipo'],
            'total': round(d['total'] or 0, 2),
            'media': round(d['media'] or 0, 2),
            'maximo': round(d['maximo'] or 0, 2),
            'minimo': round(d['minimo'] or 0, 2),
        })
    return Response(resultado)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_consolidado(request):
    from apps.alertas.models import Alerta
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    registros_mes = Registro.objects.filter(data_referencia__gte=inicio_mes)
    alertas_ativos = Alerta.objects.filter(lido=False).count()

    por_setor = (
        registros_mes
        .values('indicador__setor__codigo', 'indicador__setor__nome', 'indicador__setor__cor')
        .annotate(
            total_registros=Count('id'),
            criticos=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(status='critico')),
        )
        .order_by('-total_registros')
    )

    return Response({
        'total_registros_mes': registros_mes.count(),
        'alertas_ativos': alertas_ativos,
        'criticos_mes': registros_mes.filter(status='critico').count(),
        'setores_ativos': Setor.objects.filter(ativo=True).count(),
        'por_setor': list(por_setor),
    })
