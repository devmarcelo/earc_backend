# eARC Backend - Sistema de Gestão Empresarial Multitenant

## Visão Geral

O eARC é um sistema web multitenant responsivo desenvolvido para pequenos negócios locais. O sistema oferece funcionalidades de gestão financeira, inventário, recursos humanos e relatórios, com isolamento rigoroso entre tenants e escalabilidade para adição futura de módulos.

## Sumário

- [Arquitetura](#arquitetura)
- [Tecnologias e Ferramentas](#tecnologias-e-ferramentas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação e Configuração Local](#instalação-e-configuração-local)
- [Criação de Tenants](#criação-de-tenants)
- [Padrões de API e Respostas](#padrões-de-api-e-respostas)
- [Endpoints Principais](#endpoints-principais)
- [Logging, Trace e Monitoramento](#logging-trace-e-monitoramento)
- [Testes Automatizados](#testes-automatizados)
- [Deploy](#deploy)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Social Account Google](#social-account-google)
- [Onboarding Rápido para Novos Devs](#onboarding-rápido-para-novos-devs)
- [FAQ e Helpdesk/IA](#faq-e-helpdeskia)
- [Licença](#licença)
- [Suporte](#suporte)

---

## Arquitetura

### Multitenant

O eARC implementa uma arquitetura multitenant com isolamento rigoroso usando:

- **Schemas separados** no PostgreSQL para cada tenant
- **Tenant_id** em todas as tabelas para garantir isolamento adicional
- **Row-Level Security (RLS)** no PostgreSQL para reforçar o isolamento
- **Middleware de tenant** para identificação e roteamento correto
- **Header X-Tenant** obrigatório em todas as requisições autenticadas

## Tecnologias e Ferramentas

- **Django** 5.x + django-tenants
- **PostgreSQL** (schemas isolados)
- **DRF** (Django Rest Framework)
- **JWT** (SimpleJWT)
- **drf-spectacular** (Swagger/OpenAPI)
- **pytest/pytest-django** (testes)
- **Sentry** (monitoramento)
- **Logging** multitenant com trace_id
- **OAuth2 Google** (login social seguro)
- **dj-rest-auth**, **django-allauth** (social auth APIs)

## Estrutura do Projeto

```
backend/                # Aplicação Django
├── core/               # Módulo central (tenant, usuário, autenticação)
├── financial/          # Módulo financeiro
├── hr/                 # Módulo de recursos humanos
├── inventory/          # Módulo de inventário
├── reports/            # Módulo de relatórios
├── social/             # Integração social/login social
├── settings_app/       # Módulo de configurações
└── tests/              # Módulo de testes automatizados
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

- Mensagens de erro nunca expõem informações sensíveis (emails inexistentes, detalhes técnicos etc).

## Endpoints Principais

- Autenticação: /api/v1/auth/login/, /api/v1/auth/register/, /api/v1/auth/token/refresh/

- Login Social Google: /api/v1/auth/social/google/
  (Apenas para usuários já cadastrados e ativos)

- Documentação Swagger: /api/docs/

- OpenAPI JSON: /api/schema/

## Logging, Trace e Monitoramento

- Todos os logs trazem o schema do tenant e trace_id para rastreabilidade.

- Incidentes críticos são enviados para o Sentry, com trace_id como tag.

- Rotação de logs automática e filtros multitenant garantem rastreabilidade.

- O trace_id aparece em todas as respostas e logs para facilitar debugging (incluindo integração com IA/helpdesk).

## Testes Automatizados

- Testes com pytest + pytest-django, cobrindo:

  - Fluxo de autenticação, login social, proteção JWT, roles/permissões, cross-tenant.
  - Testes de segurança (rate limiting, brute-force, CORS, CSRF, etc).
  - Testes de endpoints críticos e isolamento de tenants.

- Para rodar todos os testes:

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
| SENTRY_DSN           | DSN do Sentry (monitoramento)     | -                                   |
| ENVIRONMENT          | Ambiente (development/production) | development                         |

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

## Social Account Google

### Como obter Client ID e Client Secret do Google para login social

1. Acesse https://console.cloud.google.com/ e selecione/crie um projeto.

2. Vá em "APIs e serviços" > "Tela de consentimento OAuth" e configure.

3. Depois, em "APIs e serviços" > "Credenciais", clique em "Criar Credenciais" > "ID do Cliente OAuth".

4. Escolha "Aplicativo da Web", defina origens e redirecionamentos autorizados (incluindo URLs locais e de produção).

5. Clique em "Criar", copie o Client ID e Client Secret.

6. Salve no arquivo .env:

   ```ini
   GOOGLE_CLIENT_ID=xxxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=xxxxxxx
   ```

7. Teste o fluxo pelo endpoint /api/v1/auth/social/google/.

#### Nota sobre segurança:

Signup social está desabilitado: apenas usuários já cadastrados podem logar via Google. O sistema nunca cria tenants ou usuários automaticamente via social login.

## Onboarding Rápido para Novos Devs

- Leia este README e confira os endpoints no /api/docs/.

- Confira exemplos de resposta/erro, padrões de trace_id, uso do header X-Tenant.

- Use o trace_id para debugging em logs, Sentry e suporte.

- Siga a organização dos módulos para criar novos apps/features.

## FAQ e Helpdesk/IA

- Documentação Swagger/OpenAPI cobre todos os endpoints e payloads.

- Mensagens de erro padronizadas facilitam integração com agentes de IA/helpdesk.

- Para dúvidas sobre integração, consulte /api/docs/ ou este README.

## Segurança

O sistema implementa várias camadas de segurança:

- **Isolamento de Tenant**: Schemas separados + tenant_id em todas as tabelas

- **Row-Level Security (RLS)** no PostgreSQL

- **Autenticação JWT** com refresh tokens

- **OAuth2** para login social

- **CORS** restrito aos domínios dos tenants

- **Rate Limiting** nas APIs

## FAQ

- Para dúvidas frequentes e troubleshooting, veja também [FAQ.md](./FAQ.md)

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Suporte

Para suporte, entre em contato com a equipe de desenvolvimento em [suporte@earc.com](mailto:suporte@earc.com).
