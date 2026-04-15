from django.db import models
from django.conf import settings


class TipoIncidente(models.TextChoices):
    QUEDA            = 'queda',          'Queda de Paciente'
    LPP              = 'lpp',            'Lesão por Pressão (LPP)'
    ERRO_MEDICACAO   = 'erro_medicacao', 'Erro de Medicação'
    IDENTIFICACAO    = 'identificacao',  'Falha na Identificação do Paciente'
    CIRURGIA         = 'cirurgia',       'Cirurgia em Local Errado'
    TRANSFUSAO       = 'transfusao',     'Reação Transfusional'
    INFECCAO         = 'infeccao',       'Infecção Associada à Assistência'
    COMUNICACAO      = 'comunicacao',    'Falha de Comunicação'
    OUTRO            = 'outro',          'Outro'


class NivelDano(models.TextChoices):
    NENHUM   = 'nenhum',   'Sem Dano'
    LEVE     = 'leve',     'Dano Leve'
    MODERADO = 'moderado', 'Dano Moderado'
    GRAVE    = 'grave',    'Dano Grave'
    OBITO    = 'obito',    'Óbito'


class StatusNotificacao(models.TextChoices):
    ABERTA     = 'aberta',     'Aberta'
    EM_ANALISE = 'em_analise', 'Em Análise'
    CONCLUIDA  = 'concluida',  'Concluída'
    ARQUIVADA  = 'arquivada',  'Arquivada'


class MetaSeguranca(models.TextChoices):
    META_1 = 'meta_1', 'Meta 1 — Identificação correta do paciente'
    META_2 = 'meta_2', 'Meta 2 — Comunicação efetiva entre profissionais'
    META_3 = 'meta_3', 'Meta 3 — Segurança de medicamentos de alta vigilância'
    META_4 = 'meta_4', 'Meta 4 — Cirurgia segura (local correto)'
    META_5 = 'meta_5', 'Meta 5 — Higiene das mãos / prevenção de infecções'
    META_6 = 'meta_6', 'Meta 6 — Prevenção de quedas e lesões'


# Mapa: tipo de incidente → meta de segurança relacionada
TIPO_META_MAP = {
    TipoIncidente.IDENTIFICACAO: MetaSeguranca.META_1,
    TipoIncidente.COMUNICACAO:   MetaSeguranca.META_2,
    TipoIncidente.ERRO_MEDICACAO: MetaSeguranca.META_3,
    TipoIncidente.CIRURGIA:      MetaSeguranca.META_4,
    TipoIncidente.INFECCAO:      MetaSeguranca.META_5,
    TipoIncidente.QUEDA:         MetaSeguranca.META_6,
    TipoIncidente.LPP:           MetaSeguranca.META_6,
}


class NotificacaoNSP(models.Model):
    setor = models.ForeignKey(
        'setores.Setor', on_delete=models.CASCADE,
        related_name='notificacoes_nsp'
    )
    tipo = models.CharField(max_length=20, choices=TipoIncidente.choices)
    meta_relacionada = models.CharField(
        max_length=10, choices=MetaSeguranca.choices,
        blank=True, help_text='Preenchido automaticamente com base no tipo'
    )
    data_ocorrencia = models.DateField()
    hora_ocorrencia = models.TimeField(null=True, blank=True)
    descricao = models.TextField()
    dano = models.CharField(max_length=10, choices=NivelDano.choices, default=NivelDano.NENHUM)
    status = models.CharField(max_length=15, choices=StatusNotificacao.choices, default=StatusNotificacao.ABERTA)
    notificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='notificacoes_enviadas'
    )
    analisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notificacoes_analisadas'
    )
    plano_acao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notificação NSP'
        verbose_name_plural = 'Notificações NSP'
        ordering = ['-data_ocorrencia', '-criado_em']

    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.setor.codigo} — {self.data_ocorrencia}'

    def save(self, *args, **kwargs):
        if not self.meta_relacionada:
            self.meta_relacionada = TIPO_META_MAP.get(self.tipo, '')
        super().save(*args, **kwargs)
