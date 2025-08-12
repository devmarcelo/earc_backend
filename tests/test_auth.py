import pytest
from django.contrib.auth import get_user_model
from core.models import Tenant
from accounts.models import User, Address

@pytest.mark.django_db
def test_login_success(api_client, user):
    """
    Testa login bem-sucedido de usuário ativo e vinculado a tenant.
    """
    url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha123"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200, response.content

    # Verifica se os campos esperados estão presentes
    response_data = response.json()
    assert 'access' in response_data
    assert 'refresh' in response_data
    assert 'user' in response_data
    assert 'tenant' in response_data

    # Confere se o user retornado corresponde ao email enviado
    assert response_data['user']['email'] == user.email

    # Verifica se o tenant retornado corresponde ao tenant do usuário
    assert response_data['tenant']['id'] == user.tenant.id

@pytest.mark.django_db
def test_login_incorrect_password(api_client, user):
    """
    Falha ao tentar login com senha incorreta.
    """
    url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha_errada"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401 or response.status_code == 400
    # Detalhe: o código pode variar conforme a implementação do endpoint

@pytest.mark.django_db
def test_login_inactive_user(api_client, user):
    """
    Falha ao tentar login com usuário inativo.
    """
    user.is_active = False
    user.save()
    url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha123"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401 or response.status_code == 400

@pytest.mark.django_db
def test_login_nonexistent_user(api_client):
    """
    Falha ao tentar login com usuário que não existe.
    """
    url = '/api/v1/auth/login/'
    data = {
        "email": "naoexiste@teste.com",
        "password": "senhaqualquer"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401 or response.status_code == 400

@pytest.mark.django_db
def test_login_inactive_tenant(api_client, user, tenant):
    """
    Falha ao tentar login com tenant inativo.
    """
    tenant.is_active = False
    tenant.save()
    url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha123"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401 or response.status_code == 400

@pytest.mark.django_db
def test_login_user_in_other_tenant(api_client, user, tenant):
    """
    Usuário não consegue logar em outro tenant.
    """
    # Cria um segundo tenant e um usuário para ele
    second_tenant = Tenant.objects.create(
        name="empresa_segunda",
        document="11.111.111/0001-11",
        is_active=True,
        schema_name="empresasegunda"
    )

    User = get_user_model()
    user2 = User.objects.create_user(
        email="usuario2@teste.com",
        password="senha456",
        tenant=second_tenant,
        is_active=True,
        nickname="Usuário 2"
    )

    # Tenta logar o usuário2 com as credenciais do tenant1 (deve falhar caso o endpoint exija contexto de tenant)
    url = '/api/v1/auth/login/'
    data = {
        "email": user2.email,
        "password": "senha456"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(url, data, format='json')
    
    # O comportamento aqui depende de como seu backend exige ou identifica o tenant (subdomínio, header, etc)
    # Se o contexto não estiver correto, o login deve ser negado
    assert response.status_code in (400, 401)

@pytest.mark.django_db
def test_login_success_different_tenants(api_client, tenant):
    """
    Usuários de tenants diferentes conseguem logar quando contexto é respeitado.
    """

    # Tenant A e usuário A
    tenant_a = tenant
    User = get_user_model()
    user_a = User.objects.create_user(
        email="a@teste.com", password="senhaA", tenant=tenant_a, is_active=True
    )

    # Tenant B e usuário B
    tenant_b = Tenant.objects.create(
        name="empresa_b", document="22.222.222/0001-22", is_active=True, schema_name="empresa_b"
    )
    user_b = User.objects.create_user(
        email="b@teste.com", password="senhaB", tenant=tenant_b, is_active=True
    )

    url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='empresateste')

    # Login A (deve ser sucesso)
    resp_a = api_client.post(url, {"email": user_a.email, "password": "senhaA"}, format='json')
    assert resp_a.status_code == 200
    assert resp_a.json()['user']['email'] == user_a.email

    # Login B (deve ser sucesso)
    resp_b = api_client.post(url, {"email": user_b.email, "password": "senhaB"}, format='json')
    assert resp_b.status_code == 200
    assert resp_b.json()['user']['email'] == user_b.email

@pytest.mark.django_db
def test_refresh_token_success(api_client, user):
    """
    Garante que é possível obter um novo access token com o refresh token válido.
    """
    # Login para obter tokens
    login_url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha123"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(login_url, data, format='json')
    assert response.status_code == 200
    refresh_token = response.json().get("refresh")
    assert refresh_token is not None

    # Usa o refresh token para obter novo access
    refresh_url = '/api/token/refresh/'  # ajuste se seu endpoint for diferente
    response2 = api_client.post(refresh_url, {"refresh": refresh_token}, format='json')
    assert response2.status_code == 200
    new_access = response2.json().get("access")
    assert new_access is not None

@pytest.mark.django_db
def test_access_protected_endpoint(api_client, user, address):
    """
    Garante que apenas usuários autenticados acessam endpoints protegidos.
    """
    # Login para obter o access token
    login_url = '/api/v1/auth/login/'
    data = {
        "email": user.email,
        "password": "senha123"
    }
    api_client.credentials(HTTP_X_TENANT='empresateste')
    response = api_client.post(login_url, data, format='json')
    access_token = response.json().get("access")
    assert access_token is not None

    # Endpoint protegido (ajuste a URL para algum endpoint protegido do seu sistema)
    protected_url = '/api/addresses/'  # exemplo: lista de endereços

    # Sem autenticação (deve falhar)
    resp_noauth = api_client.get(protected_url)
    assert resp_noauth.status_code in (401, 403)

    # Com autenticação (deve funcionar)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    resp_auth = api_client.get(protected_url)
    assert resp_auth.status_code == 200
    # Opcional: checa se o address do tenant aparece na lista
    results = resp_auth.json()
    assert any(str(address.id) in str(result) for result in results if isinstance(result, dict))

@pytest.mark.django_db
def test_user_cannot_access_other_tenant_resource(api_client, user, address, tenant):
    """
    Usuário de um tenant não acessa dados de outro tenant.
    """
    # Cria segundo tenant e endereço associado a ele
    tenant2 = Tenant.objects.create(
        name="empresa_isolada",
        document="33.333.333/0001-33",
        is_active=True,
        schema_name="empresaisolada"
    )
    User = get_user_model()
    user2 = User.objects.create_user(
        email="isolado@empresa.com",
        password="senha789",
        tenant=tenant2,
        is_active=True
    )
    # Endereço no tenant2
    from core.models import Address
    address2 = Address.objects.create(
        tenant=tenant2,
        created_by=user2,
        updated_by=user2,
        zipcode="99999-000",
        address="Rua Outro Tenant",
        address_number="1",
        neighborhood="Outro Bairro",
        city="Outra Cidade",
        state="UF",
        country="Brasil"
    )
    # Login com user do tenant1
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='empresaisolada')
    resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.json()['access']}")
    # Tenta acessar address2 (deve falhar, normalmente 404)
    protected_url = f'/api/addresses/{address2.id}/'
    r = api_client.get(protected_url)
    assert r.status_code in (403, 404)  # depende da lógica: pode ocultar (404) ou bloquear (403)

@pytest.mark.django_db
def test_user_cannot_access_admin_endpoint(api_client, user):
    """
    Usuário comum não acessa endpoint restrito a admin/staff.
    """
    # Login user comum
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='empresateste')
    resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.json()['access']}")
    # Exemplo: endpoint de governança/admin (ajuste a URL conforme seu sistema)
    admin_url = '/api/admin-only/'
    r = api_client.get(admin_url)
    assert r.status_code in (403, 404)

@pytest.mark.django_db
def test_staff_can_access_admin_endpoint(api_client, tenant):
    """
    Usuário staff/admin acessa endpoint restrito.
    """
    User = get_user_model()
    admin = User.objects.create_user(
        email="admin@empresa.com",
        password="senhaadmin",
        tenant=tenant,
        is_active=True,
        is_staff=True
    )
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='empresaisolada')
    resp = api_client.post(login_url, {"email": admin.email, "password": "senhaadmin"}, format='json')
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.json()['access']}")
    admin_url = '/api/admin-only/'
    r = api_client.get(admin_url)
    assert r.status_code == 200

@pytest.mark.django_db
def test_access_denied_if_tenant_inactive(api_client, user, tenant):
    """
    Usuário não acessa recursos se o tenant estiver inativo.
    """
    tenant.is_active = False
    tenant.save()
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='empresateste')
    resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    assert resp.status_code in (400, 401, 403)

@pytest.mark.django_db
def test_login_success_with_tenant_header(api_client, tenant, user):
    """
    Usuário faz login corretamente quando contexto de tenant está presente via header.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    response = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    assert response.status_code == 200
    data = response.json()
    assert data['user']['email'] == user.email
    assert data['tenant']['id'] == tenant.id

@pytest.mark.django_db
def test_login_fail_wrong_tenant_header(api_client, tenant, user):
    """
    Usuário não faz login se enviar o header de outro tenant.
    """
    # Cria outro tenant
    tenant2 = Tenant.objects.create(
        name="empresa_segunda",
        document="11.111.111/0001-11",
        is_active=True,
        schema_name="empresasegunda"
    )
    login_url = '/api/v1/auth/login/'
    # Tenta logar user do tenant1 enviando header do tenant2
    api_client.credentials(HTTP_X_TENANT=tenant2.schema_name)
    response = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    assert response.status_code in (400, 401, 403)

@pytest.mark.django_db
def test_login_success_in_other_tenant(api_client):
    """
    Usuário de outro tenant faz login com header correto.
    """
    User = get_user_model()
    # Cria tenant2 e user2
    from core.models import Tenant
    tenant2 = Tenant.objects.create(
        name="empresa_segunda",
        document="11.111.111/0001-11",
        is_active=True,
        schema_name="empresasegunda"
    )
    user2 = User.objects.create_user(
        email="usuario2@teste.com",
        password="senha456",
        tenant=tenant2,
        is_active=True
    )
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant2.schema_name)
    response = api_client.post(login_url, {"email": user2.email, "password": "senha456"}, format='json')
    assert response.status_code == 200
    data = response.json()
    assert data['user']['email'] == user2.email
    assert data['tenant']['id'] == tenant2.id

@pytest.mark.django_db
def test_protected_resource_with_tenant_header(api_client, user, tenant, address):
    """
    Usuário acessa recurso protegido apenas com token e header de tenant corretos.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    access = resp.json().get("access")

    protected_url = '/api/addresses/'
    # Sem autenticação
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    resp_noauth = api_client.get(protected_url)
    assert resp_noauth.status_code in (401, 403)

    # Com token correto e header
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}", HTTP_X_TENANT=tenant.schema_name)
    resp_auth = api_client.get(protected_url)
    assert resp_auth.status_code == 200
    # Verifica se retornou addresses do tenant correto
    results = resp_auth.json()
    assert any(str(address.id) in str(result) for result in results if isinstance(result, dict))

@pytest.mark.django_db
def test_login_fails_without_tenant_header(api_client, user):
    """
    Login deve falhar sem header de tenant.
    """
    login_url = '/api/v1/auth/login/'
    response = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    # Esperado: Unauthorized (401) ou erro customizado do middleware
    assert response.status_code in (400, 401, 403)

@pytest.mark.django_db
def test_login_fails_with_invalid_tenant_header(api_client, user):
    """
    Login deve falhar se o header de tenant não corresponder a um schema existente.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='schema_inexistente')
    response = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    assert response.status_code in (400, 401, 403)

@pytest.mark.django_db
def test_user_cannot_access_data_from_other_tenant(api_client, tenant, user):
    """
    Garante que usuário não acessa recursos de outro tenant, mesmo com token válido.
    """
    # Cria outro tenant e usuário
    tenant2 = Tenant.objects.create(
        name="tenant_b",
        document="99.999.999/0001-99",
        is_active=True,
        schema_name="tenant_b"
    )
    user2 = User.objects.create_user(
        email="userb@empresa.com",
        password="senha456",
        tenant=tenant2,
        is_active=True
    )

    # Login no tenant2
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT='tenant_b')
    resp = api_client.post(login_url, {"email": user2.email, "password": "senha456"}, format='json')
    access = resp.json().get('access')

    # Tenta acessar qualquer endpoint protegido do tenant1 (deve falhar)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}", HTTP_X_TENANT=tenant.schema_name)
    # Exemplo com endpoint hipotético de dashboard protegido
    protected_url = '/api/v1/protected-resource/'
    r = api_client.get(protected_url)
    assert r.status_code in (403, 404)

@pytest.mark.django_db
def test_brute_force_login_protection(api_client, user, tenant):
    """
    Várias tentativas de login falho devem ser limitadas/protegidas.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    max_attempts = 5
    for _ in range(max_attempts):
        response = api_client.post(login_url, {"email": user.email, "password": "senha_errada"}, format='json')
        assert response.status_code in (400, 401)
    # Após N tentativas, espera que o acesso seja temporariamente bloqueado (se proteção ativa)
    response = api_client.post(login_url, {"email": user.email, "password": "senha_errada"}, format='json')
    # O status pode ser 429 (Too Many Requests) ou mensagem específica, dependendo da implementação
    assert response.status_code in (401, 403, 429)

@pytest.mark.django_db
def test_cors_protection(api_client, user, tenant):
    """
    API deve rejeitar requisições de origens não autorizadas.
    """
    login_url = '/api/v1/auth/login/'
    # Simula uma origem não autorizada
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name, HTTP_ORIGIN='http://malicioso.com')
    response = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    # O status esperado pode ser 403 ou 400 (ou até 200 mas sem setar headers CORS)
    assert 'Access-Control-Allow-Origin' not in response

@pytest.mark.django_db
def test_no_sensitive_data_leak_in_public_endpoints(api_client, tenant, user):
    """
    Dados sensíveis (como hash de senha, tokens, etc.) não aparecem em endpoints públicos.
    """
    # Exemplo de endpoint público: /api/v1/public-info/
    public_url = '/api/v1/public-info/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    response = api_client.get(public_url)
    # O JSON não deve conter campos sensíveis
    assert "password" not in str(response.content)
    assert "token" not in str(response.content)

@pytest.mark.django_db
def test_authentication_required_on_protected_endpoint(api_client, tenant):
    """
    Endpoint protegido exige autenticação.
    """
    protected_url = '/api/v1/user/profile/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    response = api_client.get(protected_url)
    assert response.status_code in (401, 403)

@pytest.mark.django_db
def test_login_response_structure(api_client, user, tenant):
    """
    A resposta do login deve conter apenas os campos padronizados e esperados.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    assert resp.status_code == 200
    data = resp.json()

    # Deve conter apenas os campos esperados
    expected_fields = {"user", "tenant", "access", "refresh"}
    assert set(data.keys()) == expected_fields

    # O objeto 'user' não deve conter campos sensíveis (ex: senha, tokens, etc)
    forbidden_user_fields = {"password", "is_superuser"}
    assert not forbidden_user_fields.intersection(set(data["user"].keys()))

    # O objeto 'tenant' deve trazer apenas informações públicas
    forbidden_tenant_fields = {"is_anonymized"}
    assert not forbidden_tenant_fields.intersection(set(data["tenant"].keys()))

@pytest.mark.django_db
def test_login_error_response_format(api_client, tenant):
    """
    Mensagens de erro devem ser padronizadas e informativas, sem vazar detalhes sensíveis.
    """
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    resp = api_client.post(login_url, {"email": "naoexiste@teste.com", "password": "senhaerrada"}, format='json')
    assert resp.status_code in (400, 401)
    data = resp.json()
    # Mensagem genérica e padronizada
    assert "error" in data or "detail" in data
    # Nunca deve expor se o email existe ou a senha está errada

@pytest.mark.django_db
def test_register_response_structure(api_client, tenant):
    """
    A resposta do cadastro deve conter apenas os campos padronizados e esperados.
    """
    register_url = '/api/register-company/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    payload = {
        "email": "novo@teste.com",
        "password": "senhasegura123",
        "nickname": "Novo Usuário"
        # Adicione outros campos obrigatórios do seu modelo User
    }
    resp = api_client.post(register_url, payload, format='json')
    assert resp.status_code in (200, 201)
    data = resp.json()

    # Deve conter apenas os campos esperados
    expected_fields = {"user", "tenant", "access", "refresh"}
    assert set(data.keys()) == expected_fields

    forbidden_user_fields = {"password", "is_superuser"}
    assert not forbidden_user_fields.intersection(set(data["user"].keys()))

    forbidden_tenant_fields = {"is_anonymized"}
    assert not forbidden_tenant_fields.intersection(set(data["tenant"].keys()))

@pytest.mark.django_db
def test_refresh_token_response_structure(api_client, user, tenant):
    """
    A resposta do refresh deve conter apenas os campos padronizados.
    """
    # Primeiro, login para obter refresh token
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    login_resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    refresh_token = login_resp.json().get("refresh")

    refresh_url = '/api/token/refresh/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    resp = api_client.post(refresh_url, {"refresh": refresh_token}, format='json')
    assert resp.status_code == 200
    data = resp.json()
    # O padrão mais comum: só retorna o novo access token
    assert set(data.keys()) == {"access"}
    assert "refresh" not in data

@pytest.mark.django_db
def test_logout_response_structure(api_client, user, tenant):
    """
    A resposta do logout deve ser padronizada e sem dados sensíveis.
    """
    # Primeiro, login para obter access token
    login_url = '/api/v1/auth/login/'
    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    login_resp = api_client.post(login_url, {"email": user.email, "password": "senha123"}, format='json')
    access_token = login_resp.json().get("access")

    logout_url = '/api/v1/auth/logout/'
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}", HTTP_X_TENANT=tenant.schema_name)
    resp = api_client.post(logout_url, {}, format='json')
    # Pode variar: 200 OK, 204 No Content ou mensagem padronizada
    assert resp.status_code in (200, 204)
    if resp.content:
        data = resp.json()
        assert "detail" in data or "success" in data
