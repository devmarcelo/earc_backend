import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import Tenant, Address

@pytest.fixture
def tenant(db):
    """
    Cria e retorna um tenant válido para os testes.
    """
    return Tenant.objects.create(
        name="Empresa Teste",
        schema_name="empresateste",
        document="12.345.678/0001-99",
        is_active=True
    )

@pytest.fixture
def user(db, tenant):
    """
    Cria e retorna um usuário associado ao tenant.
    """
    User = get_user_model()
    user = User.objects.create_user(
        email="usuario@teste.com",
        password="senha123",
        tenant=tenant,
        is_active=True,
        nickname="Usuário Teste"
    )
    return user

@pytest.fixture
def address(db, tenant, user):
    """
    Cria e retorna um endereço associado ao tenant e criado pelo usuário.
    """
    return Address.objects.create(
        tenant=tenant,
        created_by=user,
        updated_by=user,
        zipcode="12345-678",
        address="Rua Teste",
        address_number="100",
        complement="Apto 10",
        neighborhood="Centro",
        city="Cidade Teste",
        state="UF",
        country="Brasil",
        is_active=True
    )

@pytest.fixture
def api_client():
    """
    Retorna um APIClient do DRF para requisições de teste.
    """
    return APIClient()
