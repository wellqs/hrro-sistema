from django.db import models
from django.conf import settings


class Modalidade(models.TextChoices):
    INTERNADO   = 'internado',   'Paciente Internado'
    UTI         = 'uti',         'UTI'
    AMBULATORIAL = 'ambulatorial', 'Ambulatorial'
    DOMICILIAR  = 'domiciliar',  'Domiciliar'


class Especialidade(models.TextChoices):
    RESPIRATORIA    = 'respiratoria',    'Fisioterapia Respiratória'
    ORTOPEDICA      = 'ortopedica',      'Fisioterapia Ortopédica'
    NEUROLOGICA     = 'neurologica',     'Fisioterapia Neurológica'
    CARDIOVASCULAR  = 'cardiovascular',  'Fisioterapia Cardiovascular'
    PEDIATRICA      = 'pediatrica',      'Fisioterapia Pediátrica'
    OUTRO           = 'outro',           'Outro'


class StatusAtendimento(models.TextChoices):
    AGENDADO     = 'agendado',     'Agendado'
    EM_ANDAMENTO = 'em_andamento', 'Em Andamento'
    REALIZADO    = 'realizado',    'Realizado'
    FALTA        = 'falta',        'Falta'
    CANCELADO    = 'cancelado',    'Cancelado'


class AtendimentoFisio(models.Model):
    setor_origem = models.ForeignKey(
        'setores.Setor', on_delete=models.CASCADE,
        related_name='atendimentos_fisio',
        help_text='Setor/ala de origem do paciente'
    )
    paciente_nome      = models.CharField(max_length=200)
    prontuario         = models.CharField(max_length=50, blank=True)
    modalidade         = models.CharField(max_length=15, choices=Modalidade.choices, default=Modalidade.INTERNADO)
    especialidade      = models.CharField(max_length=15, choices=Especialidade.choices, default=Especialidade.RESPIRATORIA)
    status             = models.CharField(max_length=15, choices=StatusAtendimento.choices, default=StatusAtendimento.AGENDADO)
    data_atendimento   = models.DateField()
    hora_inicio        = models.TimeField(null=True, blank=True)
    numero_sessao      = models.PositiveSmallIntegerField(default=1, verbose_name='N° da Sessão')
    descricao_clinica  = models.TextField(blank=True, help_text='Resumo clínico / diagnóstico')
    objetivos          = models.TextField(blank=True, help_text='Objetivos terapêuticos')
    evolucao           = models.TextField(blank=True, help_text='Evolução da sessão')
    alta_fisioterapeutica = models.BooleanField(default=False)
    profissional       = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='atendimentos_fisio'
    )
    criado_em          = models.DateTimeField(auto_now_add=True)
    atualizado_em      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Atendimento de Fisioterapia'
        verbose_name_plural = 'Atendimentos de Fisioterapia'
        ordering = ['-data_atendimento', '-criado_em']

    def __str__(self):
        return f'{self.paciente_nome} — {self.get_especialidade_display()} — {self.data_atendimento}'
