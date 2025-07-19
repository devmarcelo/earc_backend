import pytest
from django.contrib.auth import get_user_model
from core.models import Tenant
from unittest.mock import patch

@pytest.mark.django_db
def test_google_login_success(api_client, tenant, settings):
    """
    Usuário já cadastrado pode autenticar via Google OAuth.
    """
    User = get_user_model()

    user = User.objects.create_user(
        email="usergoogle@empresa.com",
        password="senhafake",
        tenant=tenant,
        is_active=True,
    )

    with requests_mock.Mocker() as m:
        # Endpoint chamado pelo allauth para obter userinfo (padrão Google OAuth2)
        m.get("https://www.googleapis.com/oauth2/v3/userinfo", json={
            "email": "usergoogle@empresa.com",
            "email_verified": True,
            "sub": "1234567890",
            "name": "Google User",
            "given_name": "Google",
            "family_name": "User",
            "locale": "pt-BR",
            "picture": "https://example.com/avatar.jpg"
        })

        payload = {
            "access_token": "mocked-valid-access-token"
        }

        api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
        url = "/api/v1/auth/social/google/"
        response = api_client.post(url, payload, format="json")

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["success"] is True
    assert "user" in data["data"]
    assert data["data"]["user"]["email"] == "usergoogle@empresa.com"

@pytest.mark.django_db
def test_google_login_denied_for_unknown_user(api_client, tenant):
    """
    Usuário não cadastrado é bloqueado no login social Google.
    """
    payload = {
        "access_token": "mocked-valid-access-token"
    }

    api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
    url = "/api/v1/auth/social/google/"
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False
    assert "Usuário não encontrado" in data["errors"]["email"]

@pytest.mark.django_db
def test_google_login_success_patch(api_client, tenant):
    User = get_user_model()
    user = User.objects.create_user(
        email="usergoogle@empresa.com",
        password="senhafake",
        tenant=tenant,
        is_active=True,
    )

    # Patcha o método que busca o userinfo na Google API
    with patch("allauth.socialaccount.providers.google.views.requests") as mock_requests:
        mock_requests.get.return_value.json.return_value = {
            "email": "usergoogle@empresa.com",
            "email_verified": True,
            "sub": "1234567890",
            "name": "Google User",
            "given_name": "Google",
            "family_name": "User",
            "locale": "pt-BR",
            "picture": "https://example.com/avatar.jpg"
        }

        payload = {
            "access_token": "mocked-valid-access-token"
        }
        
        api_client.credentials(HTTP_X_TENANT=tenant.schema_name)
        url = "/api/v1/auth/social/google/"
        response = api_client.post(url, payload, format="json")

    assert response.status_code in (200, 201)
