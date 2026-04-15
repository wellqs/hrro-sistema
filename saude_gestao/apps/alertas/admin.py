from django.contrib import admin
from .models import Alerta


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'setor', 'nivel', 'lido', 'criado_em']
    list_filter = ['nivel', 'lido', 'setor']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['criado_em', 'lido_em']
    date_hierarchy = 'criado_em'
