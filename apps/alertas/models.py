from django.db import models
from django.conf import settings


class NivelAlerta(models.TextChoices):
    INFO = 'info', 'Informação'
    ATENCAO = 'atencao', 'Atenção'
    CRITICO = 'critico', 'Crítico'


class Alerta(models.Model):
    setor = models.ForeignKey('setores.Setor', on_delete=models.CASCADE, related_name='alertas')
    registro = models.ForeignKey(
        'indicadores.Registro', on_delete=models.CASCADE,
        null=True, blank=True, related_name='alertas'
    )
    nivel = models.CharField(max_length=10, choices=NivelAlerta.choices, default=NivelAlerta.INFO)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    lido = models.BooleanField(default=False)
    lido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='alertas_lidos'
    )
    lido_em = models.DateTimeField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-criado_em']

    def __str__(self):
        return f'[{self.nivel.upper()}] {self.titulo}'

    def marcar_lido(self, usuario):
        from django.utils import timezone
        self.lido = True
        self.lido_por = usuario
        self.lido_em = timezone.now()
        self.save()
