from django.contrib import admin
from .models import AtendimentoFisio


@admin.register(AtendimentoFisio)
class AtendimentoFisioAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'prontuario', 'especialidade', 'modalidade', 'status', 'data_atendimento', 'numero_sessao', 'profissional')
    list_filter = ('status', 'especialidade', 'modalidade', 'alta_fisioterapeutica', 'data_atendimento')
    search_fields = ('paciente_nome', 'prontuario')
    date_hierarchy = 'data_atendimento'
