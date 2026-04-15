from rest_framework import serializers
from .models import SolicitacaoNIR


class SolicitacaoNIRSerializer(serializers.ModelSerializer):
    setor_codigo        = serializers.CharField(source='setor.codigo', read_only=True)
    solicitado_por_nome = serializers.SerializerMethodField()
    regulado_por_nome   = serializers.SerializerMethodField()

    class Meta:
        model = SolicitacaoNIR
        fields = [
            'id', 'setor', 'setor_codigo',
            'tipo', 'prioridade', 'status',
            'paciente_nome', 'paciente_prontuario', 'data_nascimento',
            'descricao_clinica', 'justificativa', 'cid_principal',
            'destino_solicitado',
            'solicitado_por', 'solicitado_por_nome',
            'regulado_por', 'regulado_por_nome',
            'data_solicitacao', 'data_regulacao',
            'observacoes', 'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def get_solicitado_por_nome(self, obj):
        if obj.solicitado_por:
            return obj.solicitado_por.get_full_name() or obj.solicitado_por.username
        return ''

    def get_regulado_por_nome(self, obj):
        if obj.regulado_por:
            return obj.regulado_por.get_full_name() or obj.regulado_por.username
        return ''
