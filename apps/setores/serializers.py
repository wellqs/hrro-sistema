from rest_framework import serializers
from .models import Setor


class SetorSerializer(serializers.ModelSerializer):
    parent_codigo = serializers.SerializerMethodField()
    subordinados_count = serializers.SerializerMethodField()

    class Meta:
        model = Setor
        fields = [
            'id', 'codigo', 'nome', 'tipo', 'nivel',
            'cor', 'responsavel', 'descricao', 'ativo',
            'parent', 'parent_codigo', 'subordinados_count', 'criado_em'
        ]

    def get_parent_codigo(self, obj):
        return obj.parent.codigo if obj.parent else None

    def get_subordinados_count(self, obj):
        return obj.subordinados.filter(ativo=True).count()


class SetorDetalheSerializer(SetorSerializer):
    subordinados = serializers.SerializerMethodField()

    class Meta(SetorSerializer.Meta):
        fields = SetorSerializer.Meta.fields + ['subordinados']

    def get_subordinados(self, obj):
        subs = obj.subordinados.filter(ativo=True)
        return SetorSerializer(subs, many=True).data
