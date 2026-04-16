from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Setor
from .serializers import SetorSerializer, SetorDetalheSerializer


class SetorListView(generics.ListAPIView):
    serializer_class = SetorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Setor.objects.filter(ativo=True).select_related('parent')
        tipo = self.request.query_params.get('tipo')
        nivel = self.request.query_params.get('nivel')
        if tipo:
            qs = qs.filter(tipo=tipo)
        if nivel is not None:
            qs = qs.filter(nivel=nivel)
        if not user.pode_ver_tudo:
            setor = user.setor
            if setor:
                ids_permitidos = [setor.id] + [s.id for s in setor.get_subordinados_recursivo()]
                qs = qs.filter(id__in=ids_permitidos)
        return qs


class SetorDetalheView(generics.RetrieveUpdateAPIView):
    serializer_class = SetorDetalheSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'codigo'

    def get_queryset(self):
        return Setor.objects.filter(ativo=True)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def organograma_view(request):
    setores = Setor.objects.filter(ativo=True).select_related('parent').order_by('nivel', 'nome')
    data = SetorSerializer(setores, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def resumo_setores(request):
    from apps.indicadores.models import Registro, StatusRegistro
    from apps.alertas.models import Alerta
    from django.utils import timezone
    from datetime import timedelta

    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    setores = Setor.objects.filter(ativo=True)
    resultado = []
    for setor in setores:
        alertas_ativos = Alerta.objects.filter(setor=setor, lido=False).count()
        registros_mes = Registro.objects.filter(
            indicador__setor=setor,
            data_referencia__gte=inicio_mes
        )
        criticos = registros_mes.filter(status=StatusRegistro.CRITICO).count()
        resultado.append({
            'codigo': setor.codigo,
            'nome': setor.nome,
            'tipo': setor.tipo,
            'cor': setor.cor,
            'nivel': setor.nivel,
            'alertas_ativos': alertas_ativos,
            'registros_mes': registros_mes.count(),
            'criticos': criticos,
        })
    return Response(resultado)
