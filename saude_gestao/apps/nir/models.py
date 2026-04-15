from django.db import models
from django.conf import settings


# ─── Painel de Leitos ────────────────────────────────────────────────────────

class Clinica(models.Model):
    nome       = models.CharField(max_length=100)
    capacidade = models.PositiveSmallIntegerField()
    cor        = models.CharField(max_length=7, default='#185FA5', help_text='Hex color')
    ordem      = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Clínica'
        verbose_name_plural = 'Clínicas'
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class StatusLeito(models.TextChoices):
    LIVRE     = 'livre',     'Livre'
    OCUPADO   = 'ocupado',   'Ocupado'
    RESERVADO = 'reservado', 'Reservado'
    LIMPEZA   = 'limpeza',   'Em Limpeza'
    BLOQUEADO = 'bloqueado', 'Bloqueado'


class Leito(models.Model):
    clinica        = models.ForeignKey(Clinica, on_delete=models.CASCADE, related_name='leitos')
    numero         = models.CharField(max_length=10)
    status         = models.CharField(max_length=10, choices=StatusLeito.choices, default=StatusLeito.LIVRE)
    paciente_nome  = models.CharField(max_length=200, blank=True)
    observacao     = models.CharField(max_length=300, blank=True)
    atualizado_em  = models.DateTimeField(auto_now=True)
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='leitos_atualizados'
    )

    class Meta:
        verbose_name = 'Leito'
        verbose_name_plural = 'Leitos'
        ordering = ['clinica', 'numero']
        unique_together = [('clinica', 'numero')]

    def __str__(self):
        return f'{self.clinica.nome} — {self.numero} ({self.get_status_display()})'


class TipoSolicitacao(models.TextChoices):
    TRANSFERENCIA  = 'transferencia',  'Transferência para outra unidade'
    LEITO_UTI      = 'leito_uti',      'Vaga em UTI'
    LEITO_ENFERMA  = 'leito_enferma',  'Vaga em Enfermaria'
    PROCEDIMENTO   = 'procedimento',   'Procedimento Externo'
    EXAME          = 'exame',          'Exame Externo'
    CIRURGIA       = 'cirurgia',       'Cirurgia Eletiva/Urgência'
    AMBULATORIO    = 'ambulatorio',    'Consulta Ambulatorial'
    OUTRO          = 'outro',          'Outro'


class Prioridade(models.TextChoices):
    ELETIVO    = 'eletivo',    'Eletivo'
    URGENCIA   = 'urgencia',   'Urgência'
    EMERGENCIA = 'emergencia', 'Emergência'


class StatusSolicitacao(models.TextChoices):
    SOLICITADO    = 'solicitado',    'Solicitado'
    EM_REGULACAO  = 'em_regulacao',  'Em Regulação'
    AUTORIZADO    = 'autorizado',    'Autorizado'
    NEGADO        = 'negado',        'Negado'
    CANCELADO     = 'cancelado',     'Cancelado'
    CONCLUIDO     = 'concluido',     'Concluído'


# Cores de prioridade para UI
PRIORIDADE_COR = {
    Prioridade.ELETIVO:    '#185FA5',
    Prioridade.URGENCIA:   '#BA7517',
    Prioridade.EMERGENCIA: '#A32D2D',
}


class SolicitacaoNIR(models.Model):
    setor = models.ForeignKey(
        'setores.Setor', on_delete=models.CASCADE,
        related_name='solicitacoes_nir'
    )
    tipo = models.CharField(max_length=20, choices=TipoSolicitacao.choices)
    prioridade = models.CharField(
        max_length=15, choices=Prioridade.choices,
        default=Prioridade.ELETIVO
    )
    status = models.CharField(
        max_length=15, choices=StatusSolicitacao.choices,
        default=StatusSolicitacao.SOLICITADO
    )

    # Paciente
    paciente_nome      = models.CharField(max_length=200)
    paciente_prontuario = models.CharField(max_length=50, blank=True)
    data_nascimento    = models.DateField(null=True, blank=True)

    # Clínico
    descricao_clinica  = models.TextField(help_text='Resumo clínico do paciente')
    justificativa      = models.TextField(help_text='Justificativa da solicitação')
    cid_principal      = models.CharField(max_length=10, blank=True, verbose_name='CID Principal')

    # Destino / recurso solicitado
    destino_solicitado = models.CharField(
        max_length=200, blank=True,
        help_text='Hospital, unidade ou serviço solicitado (quando aplicável)'
    )

    # Regulação
    solicitado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='solicitacoes_nir_enviadas'
    )
    regulado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='solicitacoes_nir_reguladas'
    )
    data_solicitacao = models.DateField()
    data_regulacao   = models.DateField(null=True, blank=True)
    observacoes      = models.TextField(blank=True)

    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Solicitação NIR'
        verbose_name_plural = 'Solicitações NIR'
        ordering = ['-data_solicitacao', '-criado_em']

    def __str__(self):
        return (
            f'[{self.get_tipo_display()}] {self.paciente_nome} — '
            f'{self.setor.codigo} — {self.data_solicitacao}'
        )
