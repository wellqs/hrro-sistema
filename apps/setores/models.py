from django.db import models


class TipoSetor(models.TextChoices):
    DIRECAO = 'direcao', 'Direção'
    DIRETORIA = 'diretoria', 'Diretoria'
    GERENCIA = 'gerencia', 'Gerência'
    ASSISTENCIAL = 'assistencial', 'Assistencial'
    ADMINISTRATIVO = 'administrativo', 'Administrativo'
    UNIDADE = 'unidade', 'Unidade'
    COMISSAO = 'comissao', 'Comissão'


class Setor(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TipoSetor.choices)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='subordinados'
    )
    nivel = models.IntegerField(default=0)
    cor = models.CharField(max_length=10, default='#185FA5')
    responsavel = models.CharField(max_length=150, blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nivel', 'nome']

    def __str__(self):
        return f'{self.codigo} — {self.nome}'

    def get_subordinados_recursivo(self):
        result = list(self.subordinados.filter(ativo=True))
        for sub in list(result):
            result.extend(sub.get_subordinados_recursivo())
        return result
