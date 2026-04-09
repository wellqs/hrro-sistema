# SaúdeGestão RO — Sistema de Gestão Hospitalar

Sistema web completo para gestão hospitalar por setores, desenvolvido com
**Django + Django REST Framework** no backend e **HTML + Tailwind CSS + JavaScript** no frontend.

Baseado no organograma oficial do Hospital Público de Rondônia.

---

## 🚀 Como rodar localmente

### 1. Pré-requisitos

- Python 3.10 ou superior
- pip

### 2. Instalar dependências

```bash
cd saude_gestao
pip install -r requirements.txt
```

### 3. Criar o banco de dados e aplicar migrações

```bash
python manage.py makemigrations accounts setores indicadores alertas
python manage.py migrate
```

### 4. Popular com dados iniciais

```bash
python manage.py seed_data
```

Isso cria:
- Todos os 35 setores do organograma real de Rondônia
- 9 usuários demo com diferentes perfis
- Indicadores para os principais setores
- 90 dias de registros históricos
- Alertas de exemplo

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

## 👥 Usuários de Teste

Senha padrão para todos: `hosp@2024`

| E-mail                          | Perfil    | Setor        |
|---------------------------------|-----------|--------------|
| dg@hospital.ro.gov.br           | Direção   | DG           |
| dga@hospital.ro.gov.br          | Direção   | DGA          |
| dirtec@hospital.ro.gov.br       | Diretoria | DIRTEC       |
| dass@hospital.ro.gov.br         | Diretoria | DASS         |
| genf@hospital.ro.gov.br         | Gerência  | GENF         |
| gfah@hospital.ro.gov.br         | Gerência  | GFAH         |
| uti@hospital.ro.gov.br          | Setor     | UTI          |
| lab@hospital.ro.gov.br          | Setor     | LAB          |
| ccih@hospital.ro.gov.br         | Setor     | CCIH         |
| admin@hospital.ro.gov.br        | Superuser | —            |

Superuser (senha: `admin@2024`) — acesso ao `/admin/`

---

## 📁 Estrutura do Projeto

```
saude_gestao/
├── manage.py
├── requirements.txt
├── core/
│   ├── settings.py          # Configurações Django
│   ├── urls.py              # URLs raiz
│   └── wsgi.py
├── apps/
│   ├── accounts/            # Usuários e autenticação
│   │   ├── models.py        # Modelo Usuario (custom AbstractUser)
│   │   ├── serializers.py   # JWT + UsuarioSerializer
│   │   ├── views.py         # Login/Logout HTML
│   │   ├── api_views.py     # API REST
│   │   ├── urls.py          # URLs HTML
│   │   └── api_urls.py      # URLs API
│   ├── setores/             # Estrutura organizacional
│   │   ├── models.py        # Modelo Setor com hierarquia
│   │   ├── api_views.py     # API + organograma + resumo
│   │   ├── views.py         # Views HTML (dashboard, detalhe)
│   │   ├── urls.py          # URLs API
│   │   ├── urls_views.py    # URLs HTML
│   │   └── management/commands/seed_data.py
│   ├── indicadores/         # KPIs e registros
│   │   ├── models.py        # Indicador + Registro (com auto-alerta)
│   │   ├── serializers.py
│   │   ├── api_views.py     # CRUD + gráficos + dashboard
│   │   └── urls.py
│   └── alertas/             # Sistema de notificações
│       ├── models.py        # Alerta com níveis
│       ├── api_views.py     # Listagem, marcação lido, contagem
│       └── urls.py
└── templates/
    ├── base/base.html       # Layout com sidebar, topbar
    ├── auth/login.html      # Tela de login
    ├── dashboard/
    │   ├── index.html       # Dashboard principal com gráficos
    │   └── alertas.html     # Central de alertas
    ├── setores/
    │   ├── detalhe.html     # Página do setor (indicadores, gráficos, histórico)
    │   └── organograma.html # Visualização hierárquica
    └── indicadores/
        └── registro.html    # Formulário de lançamento
```

---

## 🔌 API REST

Documentação rápida dos principais endpoints:

### Autenticação
```
POST /api/auth/token/          # Login — retorna access + refresh JWT
POST /api/auth/token/refresh/  # Renovar token
GET  /api/auth/me/             # Dados do usuário logado
```

### Setores
```
GET  /api/setores/             # Lista todos os setores
GET  /api/setores/organograma/ # Estrutura hierárquica completa
GET  /api/setores/resumo/      # Resumo com indicadores e alertas por setor
GET  /api/setores/<codigo>/    # Detalhe de um setor
```

### Indicadores e Registros
```
GET  /api/indicadores/                  # Lista indicadores
POST /api/indicadores/                  # Criar indicador
GET  /api/indicadores/registros/        # Lista registros (filtros: setor, data, status)
POST /api/indicadores/registros/        # Lançar novo registro
GET  /api/indicadores/grafico/<codigo>/ # Dados para gráfico por setor
GET  /api/indicadores/dashboard/        # Consolidado geral
```

### Alertas
```
GET  /api/alertas/                    # Lista alertas (filtros: nivel, lido, setor)
GET  /api/alertas/contagem/           # Contagem por nível
POST /api/alertas/<id>/lido/          # Marcar alerta como lido
POST /api/alertas/marcar-todos-lidos/ # Marcar todos como lidos
```

---

## 🏥 Setores Cadastrados (35 ao total)

Baseados no organograma oficial do Governo de Rondônia:

**Direção:** DG, DGA  
**Diretorias:** DIRTEC, DASS, DCLIN  
**Gerências:** GMED, GENF, GFAH, GFISIO, GFONO, GPSIC, GNUD, ASOCIAL, GEPIDEMIO, GAD  
**Assistenciais:** NIR, NOBITO, NURADIO, NSP, NSESMT, NCME, AMB, ROUP, OPME, ACOMP  
**Administrativos:** GAB, ASTEC, NRH, NOUVI  
**Unidades:** UTI, LAB  
**Comissões:** CCIH, CIPA, NEP, NCOMPEHEX  

---

## 🔐 Controle de Acesso (RBAC)

| Perfil    | Acesso                                                  |
|-----------|---------------------------------------------------------|
| Direção   | Todos os setores, dashboard consolidado, todos alertas  |
| Diretoria | Setores subordinados à sua diretoria                    |
| Gerência  | Apenas seu setor                                        |
| Setor     | Apenas seu setor                                        |

---

## ⚙️ Alertas Automáticos

O sistema gera alertas automaticamente quando um registro é salvo e o valor ultrapassa os limites configurados no indicador:

- **Atenção** → valor ≥ `limite_atencao`
- **Crítico** → valor ≥ `limite_critico`

Configure os limites em `/admin/indicadores/indicador/` ou via API.

---

## 🛠️ Próximos Passos (Produção)

1. Troque `SECRET_KEY` em `settings.py`
2. Configure `DATABASES` para PostgreSQL
3. Defina `DEBUG = False` e `ALLOWED_HOSTS`
4. Configure `EMAIL_BACKEND` para notificações por e-mail
5. Rode `python manage.py collectstatic`
6. Use Gunicorn + Nginx

```bash
# PostgreSQL (adicionar ao settings.py)
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
