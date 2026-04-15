"""
python manage.py seed_data

Popula o banco com setores, usuários demo e indicadores/registros de exemplo.
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.setores.models import Setor, TipoSetor
from apps.indicadores.models import Indicador, Registro, TipoIndicador
from apps.alertas.models import Alerta, NivelAlerta
from apps.nsp.models import NotificacaoNSP, TipoIncidente, NivelDano, StatusNotificacao

User = get_user_model()

SETORES_DATA = [
    # (codigo, nome, tipo, parent_codigo, nivel, cor)
    ('DG',        'Direção Geral',                                  'direcao',       None,      0, '#185FA5'),
    ('DGA',       'Direção Geral Adjunta',                          'direcao',       'DG',      1, '#185FA5'),
    ('DIRTEC',    'Direção Técnica',                                'direcao',       'DG',      1, '#185FA5'),
    ('DASS',      'Direção Assistencial',                           'diretoria',     'DG',      1, '#0F6E56'),
    ('GAB',       'Gabinete',                                       'administrativo','DG',      2, '#5F5E5A'),
    ('ASTEC',     'Assessoria Técnica',                             'administrativo','DG',      2, '#5F5E5A'),
    ('NRH',       'Núcleo de Recursos Humanos',                     'administrativo','DGA',     2, '#5F5E5A'),
    ('GAD',       'Gerência Administrativa',                        'administrativo','DGA',     2, '#5F5E5A'),
    ('NOUVI',     'Núcleo de Ouvidoria',                            'administrativo','DG',      2, '#5F5E5A'),
    ('NIR',       'Núcleo Interno de Regulação',                    'assistencial',  'DG',      2, '#993C1D'),
    ('NOBITO',    'Núcleo de Óbito',                                'assistencial',  'DG',      2, '#993C1D'),
    ('NURADIO',   'Núcleo de Radiologia',                           'assistencial',  'DASS',    2, '#993C1D'),
    ('NSP',       'Núcleo de Segurança do Paciente',                'assistencial',  'DGA',     2, '#993C1D'),
    ('NSESMT',    'Núcleo SESMT',                                   'assistencial',  'DG',      2, '#993C1D'),
    ('NCME',      'Núcleo CME',                                     'assistencial',  'DASS',    2, '#993C1D'),
    ('AMB',       'Central de Ambulatório',                         'assistencial',  'DG',      2, '#993C1D'),
    ('ROUP',      'Central de Rouparia',                            'assistencial',  'DG',      2, '#993C1D'),
    ('OPME',      'Central de OPME',                                'assistencial',  'DG',      2, '#993C1D'),
    ('ACOMP',     'Central de Acompanhantes',                       'assistencial',  'DG',      2, '#993C1D'),
    ('GMED',      'Gerência Médica',                                'gerencia',      'DIRTEC',  2, '#534AB7'),
    ('GENF',      'Gerência de Enfermagem',                         'gerencia',      'DASS',    2, '#534AB7'),
    ('GFAH',      'Gerência de Farmácia',                           'gerencia',      'DASS',    2, '#534AB7'),
    ('GFISIO',    'Gerência de Fisioterapia',                       'gerencia',      'DASS',    2, '#534AB7'),
    ('GFONO',     'Gerência de Fonoaudiologia',                     'gerencia',      'DASS',    2, '#534AB7'),
    ('GPSIC',     'Gerência de Psicologia',                         'gerencia',      'DASS',    2, '#534AB7'),
    ('GNUD',      'Gerência de Nutrição e Dietética',               'gerencia',      'DASS',    2, '#534AB7'),
    ('ASOCIAL',   'Gerência de Assistência Social',                 'gerencia',      'DASS',    2, '#534AB7'),
    ('GEPIDEMIO', 'Gerência de Epidemiologia',                      'gerencia',      'DG',      2, '#534AB7'),
    ('DCLIN',     'Diretoria Clínica',                              'diretoria',     'DIRTEC',  2, '#0F6E56'),
    ('UTI',       'Unidade de Terapia Intensiva (UTI)',             'unidade',       'DIRTEC',  3, '#A32D2D'),
    ('LAB',       'Laboratório',                                    'unidade',       'DASS',    3, '#A32D2D'),
    ('CCIH',      'Comissão de Controle de Infecção Hospitalar',    'comissao',      'DGA',     2, '#854F0B'),
    ('CIPA',      'Comissão Interna de Prevenção de Acidentes',     'comissao',      'DGA',     2, '#854F0B'),
    ('NEP',       'Núcleo de Educação Permanente',                  'nucleo',        'DGA',     2, '#1A6B7A'),
    ('NCOMPEHEX', 'Núcleo de Comissão de Avaliação de Plantão',     'nucleo',        'DG',      2, '#1A6B7A'),
]

INDICADORES_POR_SETOR = {
    'UTI':       [('taxa_ocupacao', 85, 95), ('eventos_adversos', 3, 6), ('obitos', None, None), ('atendimentos', None, None)],
    'LAB':       [('atendimentos', None, None), ('exames', None, None), ('tempo_resposta', 60, 120)],
    'GENF':      [('ocorrencias', 5, 10), ('atendimentos', None, None), ('qualidade', None, None)],
    'GFAH':      [('prescricoes', None, None), ('eventos_adversos', 5, 10), ('qualidade', 70, None)],
    'GMED':      [('atendimentos', None, None), ('ocorrencias', 3, 8), ('tempo_resposta', 30, 60)],
    'CCIH':      [('infeccoes', 3, 8), ('ocorrencias', None, None)],
    'NSP':       [('ocorrencias', 5, 10), ('eventos_adversos', 3, 8), ('qualidade', None, None)],
    'NURADIO':   [('exames', None, None), ('tempo_resposta', 60, 120)],
    'GEPIDEMIO': [('ocorrencias', None, None), ('atendimentos', None, None)],
    'NIR':       [('atendimentos', None, None), ('tempo_resposta', 30, 60)],
    'AMB':       [('atendimentos', None, None), ('tempo_resposta', 20, 45)],
}

USUARIOS_DEMO = [
    ('dg@hospital.ro.gov.br',    'Diretor',   'Geral',       'direcao',   'DG',      'Direção Geral'),
    ('dga@hospital.ro.gov.br',   'Diretor',   'Adjunto',     'direcao',   'DGA',     'Direção Geral Adjunta'),
    ('dirtec@hospital.ro.gov.br','Diretor',   'Técnico',     'diretoria', 'DIRTEC',  'Direção Técnica'),
    ('dass@hospital.ro.gov.br',  'Diretor',   'Assistencial','diretoria', 'DASS',    'Direção Assistencial'),
    ('genf@hospital.ro.gov.br',  'Gerente',   'Enfermagem',  'gerencia',  'GENF',    'Gerente de Enfermagem'),
    ('gfah@hospital.ro.gov.br',  'Gerente',   'Farmácia',    'gerencia',  'GFAH',    'Gerente de Farmácia'),
    ('uti@hospital.ro.gov.br',   'Coordenador','UTI',        'setor',     'UTI',     'Coordenador UTI'),
    ('lab@hospital.ro.gov.br',   'Coordenador','Laboratório','setor',     'LAB',     'Coordenador Laboratório'),
    ('ccih@hospital.ro.gov.br',  'Presidente','CCIH',        'setor',     'CCIH',    'Presidente CCIH'),
    ('nsp@hospital.ro.gov.br',   'Coordenador','NSP',        'setor',     'NSP',     'Coordenador NSP'),
]


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais do hospital'

    def handle(self, *args, **options):
        self.stdout.write('🏥 Iniciando seed do banco de dados...\n')
        self._criar_setores()
        self._criar_usuarios()
        self._criar_indicadores()
        self._criar_registros()
        self._criar_alertas_manuais()
        self._criar_notificacoes_nsp()
        self.stdout.write(self.style.SUCCESS('\n✅ Seed concluído com sucesso!\n'))
        self.stdout.write('📋 Credenciais de acesso (senha: hosp@2024):\n')
        for email, fn, ln, perfil, _, cargo in USUARIOS_DEMO:
            self.stdout.write(f'   {email}  ({perfil} — {cargo})\n')

    def _criar_setores(self):
        self.stdout.write('   Criando setores...')
        objs = {}
        # Primeira passagem: sem parent
        for codigo, nome, tipo, parent_cod, nivel, cor in SETORES_DATA:
            s, created = Setor.objects.update_or_create(
                codigo=codigo,
                defaults=dict(nome=nome, tipo=tipo, nivel=nivel, cor=cor, parent=None)
            )
            objs[codigo] = s
        # Segunda passagem: seta parents
        for codigo, nome, tipo, parent_cod, nivel, cor in SETORES_DATA:
            if parent_cod and parent_cod in objs:
                Setor.objects.filter(codigo=codigo).update(parent=objs[parent_cod])
        self.stdout.write(f' {len(SETORES_DATA)} setores OK')

    def _criar_usuarios(self):
        self.stdout.write('   Criando usuários demo...')
        for email, fn, ln, perfil, setor_cod, cargo in USUARIOS_DEMO:
            setor = Setor.objects.filter(codigo=setor_cod).first()
            user, created = User.objects.update_or_create(
                email=email,
                defaults=dict(
                    username=email.split('@')[0],
                    first_name=fn, last_name=ln,
                    perfil=perfil, setor=setor, cargo=cargo, ativo=True
                )
            )
            if created or not user.has_usable_password():
                user.set_password('hosp@2024')
                user.save()
        # superuser
        if not User.objects.filter(is_superuser=True).exists():
            su = User.objects.create_superuser(
                username='admin', email='admin@hospital.ro.gov.br',
                password='admin@2024', first_name='Admin', last_name='Sistema'
            )
            su.perfil = 'direcao'; su.save()
            self.stdout.write('   Superuser: admin@hospital.ro.gov.br / admin@2024')
        self.stdout.write(f' {len(USUARIOS_DEMO)+1} usuários OK')

    def _criar_indicadores(self):
        self.stdout.write('   Criando indicadores...')
        count = 0
        for setor_cod, inds in INDICADORES_POR_SETOR.items():
            setor = Setor.objects.filter(codigo=setor_cod).first()
            if not setor:
                continue
            for tipo, lim_at, lim_crit in inds:
                Indicador.objects.update_or_create(
                    setor=setor, tipo=tipo,
                    defaults=dict(limite_atencao=lim_at, limite_critico=lim_crit)
                )
                count += 1
        self.stdout.write(f' {count} indicadores OK')

    def _criar_registros(self):
        self.stdout.write('   Criando registros históricos (90 dias)...')
        user = User.objects.filter(is_superuser=True).first()
        hoje = date.today()
        count = 0
        VALORES_BASE = {
            'taxa_ocupacao': (60, 95), 'atendimentos': (20, 200),
            'eventos_adversos': (0, 8), 'obitos': (0, 5),
            'exames': (100, 800), 'tempo_resposta': (10, 180),
            'ocorrencias': (0, 12), 'qualidade': (60, 99),
            'infeccoes': (0, 10), 'prescricoes': (100, 500),
        }
        for indicador in Indicador.objects.select_related('setor').all():
            base = VALORES_BASE.get(indicador.tipo, (0, 100))
            for i in range(0, 90, 3):
                data = hoje - timedelta(days=i)
                valor = round(random.uniform(*base), 1)
                # Não gera alerta via signal aqui para ser mais rápido
                r = Registro(
                    indicador=indicador, valor=valor,
                    data_referencia=data, usuario=user
                )
                r.status = r._calcular_status()
                r.save()
                count += 1
        self.stdout.write(f' {count} registros OK')

    def _criar_alertas_manuais(self):
        self.stdout.write('   Criando alertas de exemplo...')
        uti = Setor.objects.filter(codigo='UTI').first()
        gfah = Setor.objects.filter(codigo='GFAH').first()
        ccih = Setor.objects.filter(codigo='CCIH').first()
        alertas = [
            (uti,  NivelAlerta.CRITICO, 'Taxa de ocupação acima do limite', 'UTI com 93% de ocupação — limite crítico de 95% próximo.'),
            (gfah, NivelAlerta.ATENCAO, 'Glosas em dispensação de medicamentos', 'GFAH: 14 glosas registradas neste mês na dispensação.'),
            (ccih, NivelAlerta.ATENCAO, '4 infecções hospitalares notificadas', 'CCIH: acompanhar protocolo de controle de infecção.'),
        ]
        for setor, nivel, titulo, desc in alertas:
            if setor:
                Alerta.objects.get_or_create(
                    setor=setor, titulo=titulo,
                    defaults=dict(nivel=nivel, descricao=desc)
                )
        self.stdout.write(f' {len(alertas)} alertas OK')

    def _criar_notificacoes_nsp(self):
        self.stdout.write('   Criando notificações NSP de exemplo...')
        user = User.objects.filter(is_superuser=True).first()
        hoje = date.today()
        notificacoes = [
            ('UTI',  TipoIncidente.QUEDA,          NivelDano.LEVE,     StatusNotificacao.EM_ANALISE, hoje - timedelta(days=5),  'Paciente caiu da cama durante a madrugada. Grade lateral estava baixa.'),
            ('UTI',  TipoIncidente.ERRO_MEDICACAO,  NivelDano.MODERADO, StatusNotificacao.ABERTA,     hoje - timedelta(days=2),  'Dose dobrada de heparina administrada por erro de leitura da prescrição.'),
            ('GENF', TipoIncidente.LPP,             NivelDano.LEVE,     StatusNotificacao.CONCLUIDA,  hoje - timedelta(days=10), 'LPP grau II identificada em paciente acamado há 7 dias. Colchão pneumático solicitado.'),
            ('GFAH', TipoIncidente.IDENTIFICACAO,   NivelDano.NENHUM,   StatusNotificacao.CONCLUIDA,  hoje - timedelta(days=15), 'Pulseira de identificação não colocada na admissão. Detectado antes de qualquer procedimento.'),
            ('NSP',  TipoIncidente.INFECCAO,        NivelDano.MODERADO, StatusNotificacao.EM_ANALISE, hoje - timedelta(days=7),  'Surto de IRAS identificado na ala cirúrgica. 3 pacientes com cultura positiva.'),
            ('NSP',  TipoIncidente.COMUNICACAO,     NivelDano.LEVE,     StatusNotificacao.ABERTA,     hoje - timedelta(days=1),  'Informação de contraindicação não repassada na passagem de plantão. Medicamento foi iniciado.'),
        ]
        count = 0
        for cod, tipo, dano, status, data, descricao in notificacoes:
            setor = Setor.objects.filter(codigo=cod).first()
            if setor:
                NotificacaoNSP.objects.get_or_create(
                    setor=setor, tipo=tipo, data_ocorrencia=data,
                    defaults=dict(dano=dano, status=status, descricao=descricao, notificado_por=user)
                )
                count += 1
        self.stdout.write(f' {count} notificações NSP OK')
