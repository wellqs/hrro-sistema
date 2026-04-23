from .models import Setor

GRUPOS_CONFIG = [
    ('direcao',        'Direção',         '#185FA5'),
    ('diretoria',      'Diretorias',      '#0F6E56'),
    ('gerencia',       'Gerências',       '#534AB7'),
    ('assistencial',   'Assistenciais',   '#993C1D'),
    ('administrativo', 'Administrativos', '#5F5E5A'),
    ('unidade',        'Unidades',        '#A32D2D'),
    ('comissao',       'Comissões',       '#854F0B'),
    ('nucleo',         'Núcleos',         '#1A6B7A'),
]

APP_ROUTES = {
    'NSP':    '/setor/nsp/',
    'NIR':    '/setor/nir/',
    'GFISIO': '/setor/gfisio/',
}


def sidebar_setores(request):
    if not request.user.is_authenticated:
        return {}
    user = request.user
    qs = Setor.objects.filter(ativo=True).order_by('nivel', 'nome')
    if not user.pode_ver_tudo:
        setor = user.setor
        if setor:
            ids = [setor.id] + [s.id for s in setor.get_subordinados_recursivo()]
            qs = qs.filter(id__in=ids)
        else:
            qs = Setor.objects.none()

    setores_list = list(qs.values('codigo', 'nome', 'tipo', 'cor'))

    # Enriquece cada setor com sua rota real
    for s in setores_list:
        s['url'] = APP_ROUTES.get(s['codigo'], f"/dashboard/setor/{s['codigo']}/")

    grupos = []
    for tipo, label, cor in GRUPOS_CONFIG:
        filhos = [s for s in setores_list if s['tipo'] == tipo]
        if filhos:
            grupos.append({'tipo': tipo, 'label': label, 'cor': cor, 'setores': filhos})

    return {'sidebar_grupos': grupos}
