from django.db import models
from django.conf import settings


class TipoIndicador(models.TextChoices):
    ATENDIMENTOS = 'atendimentos', 'Atendimentos'
    TAXA_OCUPACAO = 'taxa_ocupacao', 'Taxa de Ocupação (%)'
    EVENTOS_ADVERSOS = 'eventos_adversos', 'Eventos Adversos'
    OCORRENCIAS = 'ocorrencias', 'Ocorrências'
    TEMPO_RESPOSTA = 'tempo_resposta', 'Tempo de Resposta (min)'
    QUALIDADE = 'qualidade', 'Indicador de Qualidade (%)'
    OBITOS = 'obitos', 'Óbitos'
    INFECCOES = 'infeccoes', 'Infecções Hospitalares'
    PRESCRICOES = 'prescricoes', 'Prescrições'
    EXAMES = 'exames', 'Exames Realizados'
    PLANTOES = 'plantoes', 'Plantões'
    OUTRO = 'outro', 'Outro'


class StatusRegistro(models.TextChoices):
    NORMAL = 'normal', 'Normal'
    ATENCAO = 'atencao', 'Atenção'
    CRITICO = 'critico', 'Crítico'


class Indicador(models.Model):
    setor = models.ForeignKey('setores.Setor', on_delete=models.CASCADE, related_name='indicadores')
    tipo = models.CharField(max_length=30, choices=TipoIndicador.choices)
    nome_custom = models.CharField(max_length=100, blank=True, help_text='Nome personalizado (opcional)')
    limite_atencao = models.FloatField(null=True, blank=True, help_text='Valor a partir do qual gera alerta de atenção')
    limite_critico = models.FloatField(null=True, blank=True, help_text='Valor a partir do qual gera alerta crítico')
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        unique_together = ('setor', 'tipo')
        ordering = ['setor', 'tipo']

    def __str__(self):
        return f'{self.setor.codigo} — {self.get_tipo_display()}'

    @property
    def nome_display(self):
        return self.nome_custom or self.get_tipo_display()


class Registro(models.Model):
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, related_name='registros')
    valor = models.FloatField()
    data_referencia = models.DateField()
    observacao = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=StatusRegistro.choices, default=StatusRegistro.NORMAL)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='registros'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-data_referencia', '-criado_em']

    def __str__(self):
        return f'{self.indicador} — {self.valor} em {self.data_referencia}'

    def save(self, *args, **kwargs):
        self.status = self._calcular_status()
        super().save(*args, **kwargs)
        self._verificar_alertas()

    def _calcular_status(self):
        ind = self.indicador
        if ind.limite_critico is not None and self.valor >= ind.limite_critico:
            return StatusRegistro.CRITICO
        if ind.limite_atencao is not None and self.valor >= ind.limite_atencao:
            return StatusRegistro.ATENCAO
        return StatusRegistro.NORMAL

    def _verificar_alertas(self):
        from apps.alertas.models import Alerta, NivelAlerta
        if self.status == StatusRegistro.CRITICO:
            Alerta.objects.get_or_create(
                registro=self,
                defaults={
                    'setor': self.indicador.setor,
                    'nivel': NivelAlerta.CRITICO,
                    'titulo': f'Valor crítico em {self.indicador.nome_display}',
                    'descricao': f'{self.indicador.setor.codigo}: {self.indicador.nome_display} atingiu {self.valor} (limite: {self.indicador.limite_critico})',
                }
            )
        elif self.status == StatusRegistro.ATENCAO:
            Alerta.objects.get_or_create(
                registro=self,
                defaults={
                    'setor': self.indicador.setor,
                    'nivel': NivelAlerta.ATENCAO,
                    'titulo': f'Atenção em {self.indicador.nome_display}',
                    'descricao': f'{self.indicador.setor.codigo}: {self.indicador.nome_display} em {self.valor}',
                }
            )
