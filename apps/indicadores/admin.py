from django.contrib import admin
from .models import Indicador, Registro


@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ['setor', 'tipo', 'nome_custom', 'limite_atencao', 'limite_critico', 'ativo']
    list_filter = ['tipo', 'ativo', 'setor']
    search_fields = ['setor__codigo', 'setor__nome', 'nome_custom']


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['indicador', 'valor', 'data_referencia', 'status', 'usuario', 'criado_em']
    list_filter = ['status', 'data_referencia', 'indicador__setor']
    search_fields = ['indicador__setor__codigo']
    date_hierarchy = 'data_referencia'
    readonly_fields = ['status', 'criado_em']
