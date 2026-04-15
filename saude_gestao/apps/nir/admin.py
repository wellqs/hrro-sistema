from django.contrib import admin
from .models import SolicitacaoNIR, Clinica, Leito


class LeitoInline(admin.TabularInline):
    model  = Leito
    extra  = 0
    fields = ('numero', 'status', 'paciente_nome', 'observacao')


@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'cor', 'ordem')
    inlines      = [LeitoInline]


@admin.register(Leito)
class LeitoAdmin(admin.ModelAdmin):
    list_display  = ('numero', 'clinica', 'status', 'paciente_nome', 'atualizado_em')
    list_filter   = ('clinica', 'status')
    search_fields = ('numero', 'paciente_nome')
    readonly_fields = ('atualizado_em',)


@admin.register(SolicitacaoNIR)
class SolicitacaoNIRAdmin(admin.ModelAdmin):
    list_display  = ('paciente_nome', 'tipo', 'prioridade', 'status', 'setor', 'data_solicitacao', 'solicitado_por')
    list_filter   = ('tipo', 'prioridade', 'status', 'setor')
    search_fields = ('paciente_nome', 'paciente_prontuario', 'cid_principal', 'destino_solicitado')
    date_hierarchy = 'data_solicitacao'
    readonly_fields = ('criado_em', 'atualizado_em')
    raw_id_fields   = ('solicitado_por', 'regulado_por', 'setor')
