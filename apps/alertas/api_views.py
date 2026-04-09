from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from .models import Alerta, NivelAlerta


class AlertaSerializer(serializers.ModelSerializer):
    setor_codigo = serializers.SerializerMethodField()
    setor_nome = serializers.SerializerMethodField()

    class Meta:
        model = Alerta
        fields = [
            'id', 'setor', 'setor_codigo', 'setor_nome',
            'nivel', 'titulo', 'descricao',
            'lido', 'lido_em', 'criado_em'
        ]

    def get_setor_codigo(self, obj):
        return obj.setor.codigo

    def get_setor_nome(self, obj):
        return obj.setor.nome


class AlertaListView(generics.ListAPIView):
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Alerta.objects.select_related('setor').order_by('-criado_em')
        if not user.pode_ver_tudo and user.setor:
            qs = qs.filter(setor=user.setor)
        nivel = self.request.query_params.get('nivel')
        lido = self.request.query_params.get('lido')
        setor = self.request.query_params.get('setor')
        if nivel:
            qs = qs.filter(nivel=nivel)
        if lido is not None:
            qs = qs.filter(lido=lido.lower() == 'true')
        if setor:
            qs = qs.filter(setor__codigo=setor)
        return qs


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def marcar_lido(request, pk):
    try:
        alerta = Alerta.objects.get(pk=pk)
    except Alerta.DoesNotExist:
        return Response({'error': 'Alerta não encontrado'}, status=404)
    alerta.marcar_lido(request.user)
    return Response({'status': 'ok'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def marcar_todos_lidos(request):
    user = request.user
    from django.utils import timezone
    qs = Alerta.objects.filter(lido=False)
    if not user.pode_ver_tudo and user.setor:
        qs = qs.filter(setor=user.setor)
    qs.update(lido=True, lido_por=user, lido_em=timezone.now())
    return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def contagem_alertas(request):
    user = request.user
    qs = Alerta.objects.filter(lido=False)
    if not user.pode_ver_tudo and user.setor:
        qs = qs.filter(setor=user.setor)
    return Response({
        'total': qs.count(),
        'criticos': qs.filter(nivel=NivelAlerta.CRITICO).count(),
        'atencao': qs.filter(nivel=NivelAlerta.ATENCAO).count(),
        'info': qs.filter(nivel=NivelAlerta.INFO).count(),
    })
