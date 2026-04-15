from rest_framework import serializers
from .models import Indicador, Registro


class IndicadorSerializer(serializers.ModelSerializer):
    setor_codigo = serializers.SerializerMethodField()
    nome_display = serializers.ReadOnlyField()

    class Meta:
        model = Indicador
        fields = [
            'id', 'setor', 'setor_codigo', 'tipo', 'nome_custom',
            'nome_display', 'limite_atencao', 'limite_critico', 'ativo'
        ]

    def get_setor_codigo(self, obj):
        return obj.setor.codigo


class RegistroSerializer(serializers.ModelSerializer):
    indicador_nome = serializers.SerializerMethodField()
    setor_codigo = serializers.SerializerMethodField()
    usuario_nome = serializers.SerializerMethodField()

    class Meta:
        model = Registro
        fields = [
            'id', 'indicador', 'indicador_nome', 'setor_codigo',
            'valor', 'data_referencia', 'observacao', 'status',
            'usuario', 'usuario_nome', 'criado_em'
        ]
        read_only_fields = ['status', 'usuario', 'criado_em']

    def get_indicador_nome(self, obj):
        return obj.indicador.nome_display

    def get_setor_codigo(self, obj):
        return obj.indicador.setor.codigo

    def get_usuario_nome(self, obj):
        return obj.usuario.nome_completo if obj.usuario else '—'

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class RegistroResumoSerializer(serializers.Serializer):
    mes = serializers.CharField()
    total = serializers.FloatField()
    media = serializers.FloatField()
    maximo = serializers.FloatField()
    minimo = serializers.FloatField()
