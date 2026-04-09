from django.contrib.auth.models import AbstractUser
from django.db import models


class Perfil(models.TextChoices):
    DIRECAO = 'direcao', 'Direção'
    DIRETORIA = 'diretoria', 'Diretoria'
    GERENCIA = 'gerencia', 'Gerência'
    SETOR = 'setor', 'Setor'


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    perfil = models.CharField(max_length=20, choices=Perfil.choices, default=Perfil.SETOR)
    setor = models.ForeignKey(
        'setores.Setor',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='usuarios'
    )
    cargo = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.perfil})'

    @property
    def nome_completo(self):
        return self.get_full_name() or self.email

    @property
    def pode_ver_tudo(self):
        return self.perfil in [Perfil.DIRECAO, Perfil.DIRETORIA]

    @property
    def iniciais(self):
        parts = self.nome_completo.split()
        if len(parts) >= 2:
            return f'{parts[0][0]}{parts[-1][0]}'.upper()
        return self.nome_completo[:2].upper()
