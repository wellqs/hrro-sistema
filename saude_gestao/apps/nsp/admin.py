from django.contrib import admin
from .models import NotificacaoNSP


@admin.register(NotificacaoNSP)
class NotificacaoNSPAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'setor', 'data_ocorrencia', 'dano', 'status', 'notificado_por', 'criado_em']
    list_filter = ['tipo', 'dano', 'status', 'meta_relacionada']
    search_fields = ['descricao', 'setor__codigo', 'setor__nome']
    date_hierarchy = 'data_ocorrencia'
    readonly_fields = ['meta_relacionada', 'criado_em', 'atualizado_em']
