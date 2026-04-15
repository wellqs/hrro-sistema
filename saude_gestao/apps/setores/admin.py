from django.contrib import admin
from .models import Setor


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'tipo', 'nivel', 'parent', 'ativo']
    list_filter = ['tipo', 'nivel', 'ativo']
    search_fields = ['codigo', 'nome']
    list_editable = ['ativo']
    ordering = ['nivel', 'nome']
