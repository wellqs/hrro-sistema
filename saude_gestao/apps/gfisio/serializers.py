from rest_framework import serializers
from .models import AtendimentoFisio


class AtendimentoFisioSerializer(serializers.ModelSerializer):
    especialidade_display = serializers.CharField(source='get_especialidade_display', read_only=True)
    modalidade_display    = serializers.CharField(source='get_modalidade_display', read_only=True)
    status_display        = serializers.CharField(source='get_status_display', read_only=True)
    setor_codigo          = serializers.CharField(source='setor_origem.codigo', read_only=True)
    profissional_nome     = serializers.SerializerMethodField()

    class Meta:
        model = AtendimentoFisio
        fields = '__all__'

    def get_profissional_nome(self, obj):
        if obj.profissional:
            return f'{obj.profissional.first_name} {obj.profissional.last_name}'.strip()
        return ''
