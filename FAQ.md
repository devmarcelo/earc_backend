# eARC Backend - Sistema de Gestão Empresarial Multitenant

## FAQ – Perguntas Frequentes (eARC Backend)

### Onboarding & Ambiente de Desenvolvimento

1. Como faço o setup do projeto localmente?

Siga o passo a passo da seção Instalação e Configuração Local.

- Dúvidas comuns:

  - Confira se o Python e o PostgreSQL estão na versão exigida.
  - Use sempre .env para variáveis sensíveis.

2. Recebo erro “Database schema not set” ao rodar migrações. O que fazer?

Esse erro ocorre quando um comando roda fora do contexto de um tenant/schema.

- Use python manage.py migrate_schemas --shared para migrar apenas o schema público.

- Cheque se todos os tenants/domínios estão válidos e ativos.

3. Como criar um novo tenant e domínio para testes?

Veja exemplo na seção Criação de Tenants ou use o Django Admin.

### API, Autenticação & Segurança

4. Como funciona o login social Google?

- Apenas usuários previamente cadastrados podem acessar via Google.

- Signup social está desabilitado (ninguém cria conta nova só autenticando pelo Google).

- Caso o email Google não exista, a API retorna erro padronizado.

5. Estou recebendo “X-Tenant header required”. O que é isso?

- O header X-Tenant é obrigatório em toda requisição autenticada.

- Deve conter o schema_name do tenant ao qual o usuário pertence.

6. Por que a resposta da API traz um trace_id?

- O trace_id facilita rastreamento de erros, auditoria e suporte (incluindo integração com Sentry e helpdesk/IA).

- Use esse valor ao solicitar suporte técnico.

7. Como funcionam as mensagens de erro?

- Sempre padronizadas:

  ```json
  {
     "success": false,
     "message": "Mensagem amigável de erro",
     "errors": { ... },
     "trace_id": "uuid-123..."
  }
  ```

- Erros nunca expõem detalhes técnicos ou informações sensíveis.

### Integração, Frontend & Suporte

8. Como descubro os endpoints da API e exemplos de uso?

- Toda a documentação está disponível em /api/docs/ (Swagger/OpenAPI).

- Exemplos de requests/responses estão no README e no Swagger.

9. O login social Google retorna erro “redirect_uri_mismatch”. O que fazer?

- Confirme se o URI de redirecionamento no Google Cloud Console é igual ao configurado no backend/frontend.

- Veja Social Account Google para detalhes.

10. Como reportar um bug ou pedir suporte?

- Envie logs com trace_id, versão da API, payload (anonimizado) e uma descrição do cenário para [suporte@earc.com](mailto:suporte@earc.com).

### Administração & Multitenancy

11. Um usuário pode acessar mais de um tenant?

- Por padrão, cada usuário está vinculado a um único tenant.

- Fluxos de multi-tenant cross-user podem ser implementados sob demanda e com regras de segurança.

12. Como ativar/desativar um tenant?

- Atualmente via Django Admin ou diretamente no banco de dados.

- Futuramente, haverá painel administrativo global.

### Logging, Auditoria e Compliance

13. Onde encontro os logs do sistema?

- Logs em tempo real aparecem no console.

- Arquivos rotacionados ficam em /logs/.

- Logs trazem sempre o schema do tenant e trace_id.

14. Como funciona o monitoramento com Sentry?

- Exceções críticas são enviadas ao Sentry, associadas ao trace_id.

- O time de suporte pode investigar incidentes rapidamente.

### FAQ para IA Helpdesk (prompts para LLMs)

- “Explique como funciona o login social Google no eARC.”

- “Como identificar o trace_id de uma resposta e usá-lo para troubleshooting?”

- “O que fazer quando recebo erro de tenant não encontrado?”

- “Quais endpoints estão disponíveis para autenticação e gerenciamento de usuários?”

- “Como cadastrar um novo tenant e domínio?”
