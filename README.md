# eARC Backend - Sistema de Gestão Empresarial Multitenant

## Visão Geral

O eARC é um sistema web multitenant responsivo desenvolvido para pequenos negócios locais. O sistema oferece funcionalidades de gestão financeira, inventário, recursos humanos e relatórios, com isolamento rigoroso entre tenants e escalabilidade para adição futura de módulos.

## Arquitetura

### Multitenant

O eARC implementa uma arquitetura multitenant com isolamento rigoroso usando:

- **Schemas separados** no PostgreSQL para cada tenant

- **Tenant_id** em todas as tabelas para garantir isolamento adicional

- **Row-Level Security (RLS)** no PostgreSQL para reforçar o isolamento

- **Middleware de tenant** para identificação e roteamento correto

## Tecnologias e Ferramentas

- **Django** 5.x + django-tenants
- **PostgreSQL** (schemas isolados)
- **DRF** (Django Rest Framework)
- **JWT** (SimpleJWT)
- **drf-spectacular** (Swagger/OpenAPI)
- **pytest/pytest-django** (testes)
- **Sentry** (monitoramento)
- **Logging** multitenant com trace_id

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

## Instalação e Configuração Local

1. Instale dependências:

   ```sh
   pip install -r requirements.txt
   ```

2. Configure seu .env (use .env.example como base).

3. Execute as migrations:

```sh
python manage.py migrate_schemas
```

4. Crie um superuser:

```sh
python manage.py createsuperuser --schema=empresa_admin
```

5. Rode o servidor:

```sh
python manage.py runserver
```

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

## Padrões de API

- Toda resposta traz success, message, e opcionalmente trace_id.

- Erros sempre no padrão:

  ```json
  {
    "success": false,
    "message": "Mensagem amigável de erro",
    "errors": { ... },
    "trace_id": "uuid-123..."
  }
  ```

- O header X-Tenant é obrigatório em todas as requests autenticadas.

## Endpoints Principais

- Autenticação: /api/v1/auth/login/, /api/v1/auth/register/, /api/v1/auth/token/refresh/

- Documentação Swagger: /api/docs/

- OpenAPI JSON: /api/schema/

## Logging e Trace

- Todos os logs trazem o schema do tenant e trace_id para rastreabilidade.

- Incidentes críticos são enviados para o Sentry, com trace_id como tag.

## Testes

- Rode todos os testes:

  ```sh
  pytest
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

| Variável             | Descrição                         | Valor Padrão                        |
| -------------------- | --------------------------------- | ----------------------------------- |
| DJANGO_SECRET_KEY    | Chave secreta para o Django       | django-insecure-placeholder-for-dev |
| DJANGO_DEBUG         | Modo de depuração                 | True                                |
| DB_NAME              | Nome do banco de dados            | earc_db                             |
| DB_USER              | Usuário do banco de dados         | earc_user                           |
| DB_PASSWORD          | Senha do banco de dados           | password                            |
| DB_HOST              | Host do banco de dados            | localhost                           |
| DB_PORT              | Porta do banco de dados           | 5432                                |
| GOOGLE_CLIENT_ID     | ID do cliente OAuth do Google     | -                                   |
| GOOGLE_CLIENT_SECRET | Secret do cliente OAuth do Google | -                                   |
| GITHUB_CLIENT_ID     | ID do cliente OAuth do GitHub     | -                                   |
| GITHUB_CLIENT_SECRET | Secret do cliente OAuth do GitHub | -                                   |

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
