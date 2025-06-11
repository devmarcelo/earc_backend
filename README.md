# eARC - Sistema de Gestão Empresarial Multitenant

## Visão Geral

O eARC é um sistema web multitenant responsivo desenvolvido para pequenos negócios locais. O sistema oferece funcionalidades de gestão financeira, inventário, recursos humanos e relatórios, com isolamento rigoroso entre tenants e escalabilidade para adição futura de módulos.

## Arquitetura

### Multitenant

O eARC implementa uma arquitetura multitenant com isolamento rigoroso usando:

- **Schemas separados** no PostgreSQL para cada tenant

- **Tenant_id** em todas as tabelas para garantir isolamento adicional

- **Row-Level Security (RLS)** no PostgreSQL para reforçar o isolamento

- **Middleware de tenant** para identificação e roteamento correto

### Stack Tecnológica

#### Backend

- **Django (Python)** com middleware de tenant (django-tenant-schemas)

- **PostgreSQL** com schemas separados por tenant

- Autenticação: JWT + OAuth2 (Google/GitHub via django-allauth)

- APIs RESTful com isolamento por tenant em todas as queries

- Documentação OpenAPI/Swagger

## Estrutura do Projeto

```
backend/                # Aplicação Django
├── core/               # Módulo central (tenant, usuário, autenticação)
├── financial/          # Módulo financeiro
├── inventory/          # Módulo de inventário
├── hr/                 # Módulo de recursos humanos
├── reports/            # Módulo de relatórios
└── settings_app/       # Módulo de configurações
```

## Requisitos

- Python 3.11+

- Node.js 20+

- PostgreSQL 14+

- Ambiente virtual Python (venv)

## Instalação e Configuração

### Backend (Django)

1. Clone o repositório:

2. Crie e ative um ambiente virtual:

3. Instale as dependências:

4. Configure o banco de dados PostgreSQL:

5. Configure as variáveis de ambiente (crie um arquivo `.env` na raiz do backend):

7. Execute as migrações:

8. Crie um superusuário:

9. Inicie o servidor de desenvolvimento:

## Criação de Tenants

Para criar um novo tenant, você pode usar o Django Admin ou o shell(uma tela para cadastro de tenants será desenvolvida):

```python
# Via shell Django
python manage.py shell
from core.models import Tenant, Domain
tenant = Tenant(schema_name='cliente1', name='Cliente 1')
tenant.save()
domain = Domain(domain='cliente1.localhost', tenant=tenant, is_primary=True)
domain.save()
```

## Deploy

### Backend

1. Configure o servidor web (Nginx + Gunicorn):

2. Configure o Gunicorn:

3. Configure o PostgreSQL para produção:
  - Ative o Row-Level Security
  - Configure backups regulares
  - Otimize para performance

## Variáveis de Ambiente

### Backend

| Variável | Descrição | Valor Padrão |
| --- | --- | --- |
| DJANGO_SECRET_KEY | Chave secreta para o Django | django-insecure-placeholder-for-dev |
| DJANGO_DEBUG | Modo de depuração | True |
| DB_NAME | Nome do banco de dados | earc_db |
| DB_USER | Usuário do banco de dados | earc_user |
| DB_PASSWORD | Senha do banco de dados | password |
| DB_HOST | Host do banco de dados | localhost |
| DB_PORT | Porta do banco de dados | 5432 |
| GOOGLE_CLIENT_ID | ID do cliente OAuth do Google | - |
| GOOGLE_CLIENT_SECRET | Secret do cliente OAuth do Google | - |
| GITHUB_CLIENT_ID | ID do cliente OAuth do GitHub | - |
| GITHUB_CLIENT_SECRET | Secret do cliente OAuth do GitHub | - |

## Funcionalidades Principais

### Módulo Financeiro

- Gestão de clientes e fornecedores

- Lançamento de receitas e despesas

- Controle de contas a pagar e receber

- Conciliação bancária

### Módulo de Inventário

- Gestão de produtos e serviços

- Controle de estoque

- Movimentações de entrada e saída

### Módulo de RH

- Cadastro de funcionários

- Gestão de cargos e salários

- Controle de férias e licenças

### Módulo de Relatórios

- Dashboard personalizado

- Relatórios financeiros

- Gráficos de desempenho

- Exportação de dados

## Segurança

O sistema implementa várias camadas de segurança:

- **Isolamento de Tenant**: Schemas separados + tenant_id em todas as tabelas

- **Row-Level Security (RLS)** no PostgreSQL

- **Autenticação JWT** com refresh tokens

- **OAuth2** para login social

- **CORS** restrito aos domínios dos tenants

- **Rate Limiting** nas APIs

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte, entre em contato com a equipe de desenvolvimento em [suporte@earc.com](mailto:suporte@earc.com).

