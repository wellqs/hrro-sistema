from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nome_completo', 'perfil', 'setor', 'ativo']
    list_filter = ['perfil', 'ativo', 'setor']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Hospitalares', {'fields': ('perfil', 'setor', 'cargo', 'telefone', 'ativo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados Hospitalares', {'fields': ('email', 'perfil', 'setor', 'cargo')}),
    )
