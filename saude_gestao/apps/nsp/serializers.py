from rest_framework import serializers
from .models import NotificacaoNSP


class NotificacaoNSPSerializer(serializers.ModelSerializer):
    setor_codigo = serializers.SerializerMethodField()
    setor_nome = serializers.SerializerMethodField()
    tipo_display = serializers.SerializerMethodField()
    dano_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    meta_display = serializers.SerializerMethodField()
    notificado_por_nome = serializers.SerializerMethodField()

    class Meta:
        model = NotificacaoNSP
        fields = [
            'id', 'setor', 'setor_codigo', 'setor_nome',
            'tipo', 'tipo_display', 'meta_relacionada', 'meta_display',
            'data_ocorrencia', 'hora_ocorrencia', 'descricao',
            'dano', 'dano_display', 'status', 'status_display',
            'notificado_por', 'notificado_por_nome',
            'analisado_por', 'plano_acao',
            'criado_em', 'atualizado_em',
        ]
        read_only_fields = ['meta_relacionada', 'notificado_por', 'criado_em', 'atualizado_em']

    def get_setor_codigo(self, obj):
        return obj.setor.codigo

    def get_setor_nome(self, obj):
        return obj.setor.nome

    def get_tipo_display(self, obj):
        return obj.get_tipo_display()

    def get_dano_display(self, obj):
        return obj.get_dano_display()

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_meta_display(self, obj):
        return obj.get_meta_relacionada_display() if obj.meta_relacionada else ''

    def get_notificado_por_nome(self, obj):
        return obj.notificado_por.nome_completo if obj.notificado_por else '—'

    def create(self, validated_data):
        validated_data['notificado_por'] = self.context['request'].user
        return super().create(validated_data)
