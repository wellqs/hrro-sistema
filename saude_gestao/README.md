# SaúdeGestão RO — Sistema de Gestão Hospitalar

**Repositório:** https://github.com/wellqs/hrro-sistema

Sistema web completo para gestão hospitalar por setores, desenvolvido com
**Django + Django REST Framework** no backend e **HTML + Tailwind CSS + JavaScript** no frontend.

Baseado no organograma oficial do Hospital Público de Rondônia.

---

## Sumário

- [Como rodar localmente](#como-rodar-localmente)
- [Docker](#docker)
- [Usuários de Teste](#usuários-de-teste)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Módulos Funcionais](#módulos-funcionais)
- [API REST](#api-rest)
- [Controle de Acesso (RBAC)](#controle-de-acesso-rbac)
- [Alertas Automáticos](#alertas-automáticos)
- [Setores Cadastrados](#setores-cadastrados)
- [Próximos Passos (Produção)](#próximos-passos-produção)

---

## Como rodar localmente

### Pré-requisitos

- Python 3.10 ou superior
- pip

### 1. Instalar dependências

```bash
cd saude_gestao
pip install -r requirements.txt
```

### 2. Criar o banco de dados e aplicar migrações

```bash
python manage.py makemigrations accounts setores indicadores alertas nsp nir
python manage.py migrate
```

### 3. Popular com dados iniciais

```bash
python manage.py seed_data
```

Isso cria:
- Todos os 35 setores do organograma real de Rondônia
- 10 usuários demo com diferentes perfis
- Indicadores para os principais setores
- 90 dias de registros históricos com valores aleatórios
- Alertas gerados automaticamente para registros fora dos limites
- Notificações de exemplo para o NSP

### 4. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

## Docker

```bash
docker-compose up --build
```

O `docker-compose.yml` sobe o servidor Django na porta `8000`.

---

## Usuários de Teste

Senha padrão para todos: `hosp@2024`

| E-mail                          | Perfil    | Setor        |
|---------------------------------|-----------|--------------|
| dg@hospital.ro.gov.br           | Direção   | DG           |
| dga@hospital.ro.gov.br          | Direção   | DGA          |
| dirtec@hospital.ro.gov.br       | Diretoria | DIRTEC       |
| dass@hospital.ro.gov.br         | Diretoria | DASS         |
| dclin@hospital.ro.gov.br        | Diretoria | DCLIN        |
| genf@hospital.ro.gov.br         | Gerência  | GENF         |
| gfah@hospital.ro.gov.br         | Gerência  | GFAH         |
| uti@hospital.ro.gov.br          | Setor     | UTI          |
| lab@hospital.ro.gov.br          | Setor     | LAB          |
| ccih@hospital.ro.gov.br         | Setor     | CCIH         |

Superuser — acesso ao `/admin/`:

| E-mail                          | Senha       |
|---------------------------------|-------------|
| admin@hospital.ro.gov.br        | admin@2024  |

---

## Estrutura do Projeto

```
saude_gestao/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── core/
│   ├── settings.py              # Configurações Django (JWT, CORS, RBAC)
│   ├── urls.py                  # Roteador raiz
│   ├── wsgi.py
│   └── templates/
│       └── base/
│           └── base.html        # Layout com sidebar, topbar, Chart.js
└── apps/
    ├── accounts/                # Autenticação e usuários
    │   ├── models.py            # Usuario (AbstractBaseUser, perfil, setor, cargo)
    │   ├── serializers.py       # JWT customizado + UsuarioSerializer
    │   ├── views.py             # Login / Logout HTML
    │   ├── api_views.py         # /api/auth/
    │   ├── urls.py              # URLs HTML
    │   └── api_urls.py          # URLs API
    ├── setores/                 # Estrutura organizacional
    │   ├── models.py            # Setor (hierarquia recursiva, 9 tipos)
    │   ├── admin.py
    │   ├── serializers.py
    │   ├── api_views.py         # Lista, organograma, resumo, detalhe
    │   ├── views.py             # Dashboard, detalhe, organograma, hub
    │   ├── urls.py              # URLs API
    │   ├── urls_views.py        # URLs HTML
    │   ├── context_processors.py# Injeta sidebar_grupos em todos os templates
    │   └── management/
    │       └── commands/
    │           └── seed_data.py # Seed completo (35 setores, usuários, dados)
    ├── indicadores/             # KPIs e lançamentos
    │   ├── models.py            # Indicador + Registro (auto-calcula status e alerta)
    │   ├── serializers.py
    │   ├── api_views.py         # CRUD, gráficos, dashboard consolidado
    │   └── urls.py
    ├── alertas/                 # Notificações automáticas
    │   ├── models.py            # Alerta (nível, lido, registro referenciado)
    │   ├── serializers.py
    │   ├── api_views.py         # Listagem, contagem, marcar lido
    │   └── urls.py
    ├── nsp/                     # Núcleo de Segurança do Paciente
    │   ├── models.py            # NotificacaoNSP (tipo, dano, meta, status)
    │   ├── serializers.py
    │   ├── api_views.py         # CRUD, análise, dashboard NSP
    │   ├── views.py             # Dashboard, listas, formulários HTML
    │   ├── urls.py              # URLs API
    │   └── urls_views.py        # URLs HTML
    └── nir/                     # Núcleo Interno de Regulação
        ├── models.py            # SolicitacaoNIR + Clinica + Leito (painel de leitos)
        ├── serializers.py
        ├── api_views.py         # CRUD, regulação, painel de leitos, dashboard NIR
        ├── views.py             # Dashboard, listas, formulários HTML
        ├── urls.py              # URLs API
        └── urls_views.py        # URLs HTML
```

---

## Módulos Funcionais

### Dashboard Principal (`/dashboard/`)
Visão consolidada com:
- Total de registros, alertas ativos, críticos e setores em operação
- Gráficos de indicadores por setor (Chart.js)
- Alertas recentes com link para detalhes

### Setores (`/dashboard/setor/<codigo>/`)
Por setor:
- Indicadores e histórico de registros
- Gráficos de tendência mensal
- Subordinados e hierarquia
- Lançamento rápido de novos registros

### Organograma (`/dashboard/organograma/`)
Visualização em árvore da hierarquia hospitalar completa.

### Central de Alertas (`/dashboard/alertas/`)
Filtros por nível (info / atenção / crítico), lido/não lido e setor.
Marcação individual ou em lote como lido.

### NSP — Núcleo de Segurança do Paciente (`/setor/nsp/`)
- Dashboard com gráficos por tipo, dano, meta e tendência mensal
- Lista e formulário de notificações de incidentes
- Fluxo de análise com plano de ação
- Metas Internacionais de Segurança do Paciente (6 metas OMS)

Tipos de incidente: queda, lesão por pressão, erro de medicação, identificação, cirurgia segura, transfusão, infecção, comunicação, outro.

### NIR — Núcleo Interno de Regulação (`/setor/nir/`)
- Dashboard com solicitações por tipo, prioridade e status
- Painel de Leitos em tempo real (clínicas × leitos, atualização via PATCH)
- Lista e formulário de solicitações de regulação
- Fluxo de regulação com atualização de status

---

## API REST

Todos os endpoints requerem autenticação JWT (`Authorization: Bearer <token>`).
Exceção: `/api/auth/token/` (login).

### Autenticação — `/api/auth/`

```
POST   /api/auth/token/          Login — retorna access (8h) + refresh (1d)
POST   /api/auth/token/refresh/  Renovar token de acesso
GET    /api/auth/me/             Dados do usuário autenticado
GET    /api/auth/usuarios/       Lista usuários (filtro: perfil, setor)
```

### Setores — `/api/setores/`

```
GET    /api/setores/             Lista setores (filtro: tipo, nivel)
GET    /api/setores/organograma/ Hierarquia completa em JSON
GET    /api/setores/resumo/      Resumo por setor: alertas, registros, críticos
GET    /api/setores/<codigo>/    Detalhe do setor + subordinados
```

### Indicadores — `/api/indicadores/`

```
GET    /api/indicadores/                   Lista indicadores (filtro: setor)
POST   /api/indicadores/                   Criar indicador
GET    /api/indicadores/registros/         Lista registros (filtro: setor, data, status, indicador)
POST   /api/indicadores/registros/         Lançar registro (auto-calcula status, gera alerta)
GET    /api/indicadores/registros/<id>/    Detalhe do registro
PATCH  /api/indicadores/registros/<id>/    Atualizar / remover registro
GET    /api/indicadores/grafico/<codigo>/  Agregados mensais por setor (total, média, máx, mín)
GET    /api/indicadores/dashboard/         Consolidado geral
```

### Alertas — `/api/alertas/`

```
GET    /api/alertas/                     Lista alertas (filtro: nivel, lido, setor)
GET    /api/alertas/contagem/            Contagem de não lidos por nível
POST   /api/alertas/<id>/lido/           Marcar alerta como lido
POST   /api/alertas/marcar-todos-lidos/  Marcar todos como lidos
```

### NSP — `/api/setor/nsp/`

```
GET    /api/setor/nsp/notificacoes/                Lista notificações (filtro: tipo, dano, status, setor)
POST   /api/setor/nsp/notificacoes/                Criar notificação de incidente
GET    /api/setor/nsp/notificacoes/<id>/           Detalhe da notificação
PATCH  /api/setor/nsp/notificacoes/<id>/           Atualizar notificação
POST   /api/setor/nsp/notificacoes/<id>/analisar/  Registrar análise e plano de ação
GET    /api/setor/nsp/dashboard/                   Dashboard NSP (métricas, gráficos, tendência)
```

### NIR — `/api/setor/nir/`

```
GET    /api/setor/nir/solicitacoes/                Lista solicitações (filtro: tipo, prioridade, status, setor)
POST   /api/setor/nir/solicitacoes/                Criar solicitação de regulação
GET    /api/setor/nir/solicitacoes/<id>/           Detalhe da solicitação
PATCH  /api/setor/nir/solicitacoes/<id>/           Atualizar solicitação
POST   /api/setor/nir/solicitacoes/<id>/regular/   Regulação: atualiza status e regulador
GET    /api/setor/nir/dashboard/                   Dashboard NIR (métricas, emergências abertas)
GET    /api/setor/nir/painel/                      Painel de leitos (clínicas e status dos leitos)
PATCH  /api/setor/nir/leitos/<id>/status/          Atualizar status e paciente de um leito
```

---

## Controle de Acesso (RBAC)

| Perfil    | Acesso                                                  |
|-----------|---------------------------------------------------------|
| Direção   | Todos os setores, dashboard consolidado, todos alertas  |
| Diretoria | Setores subordinados à sua diretoria (recursivo)        |
| Gerência  | Apenas seu setor                                        |
| Setor     | Apenas seu setor                                        |

A propriedade `pode_ver_tudo` no modelo `Usuario` é `True` para perfis **Direção** e **Diretoria**.
Todas as API views filtram os querysets com base nessa propriedade automaticamente.

---

## Alertas Automáticos

O sistema gera alertas automaticamente ao salvar um `Registro`:

1. `Registro.save()` compara `valor` com os limites do `Indicador`
2. Se `valor >= limite_critico` → status `CRITICO`
3. Se `valor >= limite_atencao` → status `ATENCAO`
4. Se status != NORMAL → `Alerta.objects.get_or_create(...)` com nível correspondente

Configure os limites em `/admin/indicadores/indicador/` ou via API (`POST /api/indicadores/`).

---

## Setores Cadastrados

35 setores baseados no organograma oficial do Governo de Rondônia:

| Tipo           | Setores                                                                          |
|----------------|----------------------------------------------------------------------------------|
| Direção        | DG, DGA                                                                          |
| Diretoria      | DIRTEC, DASS, DCLIN                                                              |
| Gerência       | GMED, GENF, GFAH, GFISIO, GFONO, GPSIC, GNUD, ASOCIAL, GEPIDEMIO, GAD          |
| Assistencial   | AMB, ROUP, OPME, ACOMP, NOBITO, NURADIO                                         |
| Administrativo | GAB, ASTEC, NRH, NOUVI                                                           |
| Unidade        | UTI, LAB                                                                         |
| Comissão       | CCIH, CIPA, NEP, NCOMPEHEX                                                       |
| Núcleo         | NIR, NSP, NSESMT, NCME                                                           |

---

## Stack Técnica

**Backend**
- Django 4.2+
- Django REST Framework 3.14+
- djangorestframework-simplejwt (JWT, 8h acesso / 1d refresh, rotação automática)
- django-cors-headers
- SQLite (desenvolvimento) → PostgreSQL (produção)

**Frontend**
- HTML5 + Django Templates
- Tailwind CSS 4.4 (CDN)
- Chart.js 4.4 (gráficos)
- JavaScript vanilla (sem build step)
- Google Fonts: DM Sans, DM Mono

---

## Próximos Passos (Produção)

1. Troque `SECRET_KEY` em `settings.py` (use variável de ambiente)
2. Configure `DATABASES` para PostgreSQL
3. Defina `DEBUG = False` e `ALLOWED_HOSTS` corretos
4. Configure `EMAIL_BACKEND` para notificações por e-mail
5. Rode `python manage.py collectstatic`
6. Use Gunicorn + Nginx

```bash
# PostgreSQL (settings.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saude_gestao',
        'USER': 'postgres',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
