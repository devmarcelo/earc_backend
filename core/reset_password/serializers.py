import base64
import json
import os
import logging
from django.contrib.auth import get_user_model
from django.template import TemplateDoesNotExist
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from core.reset_password.tokens import password_reset_token_generator
from core.models import Tenant
from django_tenants.utils import schema_context
from setup import settings

User = get_user_model()
logger = logging.getLogger("core.security")

def encode_b64url(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_b64url(data: str) -> dict:
    try:
        return json.loads(base64.urlsafe_b64decode(data.encode()).decode())
    except Exception:
        raise serializers.ValidationError(_("Parâmetros inválidos ou corrompidos."))
    
FRONT_PORT = int(os.getenv("FRONT_PORT", "5173"))
    
def _build_front_url(request, tenant_schema: str) -> str:
    scheme = "http" if not request.is_secure() else "https"
    parent = getattr(settings, "PARENT_DOMAIN", "localhost")
    return f"{scheme}://{tenant_schema}.{parent}:{FRONT_PORT}"

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        tenant = self.context['request'].tenant
        if not tenant or tenant.schema_name == "public":
            raise serializers.ValidationError(_("Tenant não identificado."))
        return value

    def save(self):
        email = self.validated_data["email"]
        tenant = self.context['request'].tenant
        try:
            user = User.objects.get(email=email, tenant=tenant, is_active=True)
            token = password_reset_token_generator.make_token(user)
            payload = {
                "token": token,
                "email": user.email,
                "tenant": tenant.schema_name,
            }
            b64params = encode_b64url(payload)
            # Monta domínio dinâmico
            reset_domain = _build_front_url(self.context["request"], tenant.schema_name)
            reset_url = f"{reset_domain}/reset-password/?{b64params}"
            # E-mail context
            from core.services.email_service.sender import send_html_email
            context = {
                "tenant_logo": tenant.logo or "",
                "tenant_name": tenant.name,
                "reset_url": reset_url,
                "earc_logo": getattr(settings, "EARC_LOGO_URL", ""),  # Configure no settings.py
            }

            try:
                send_html_email(
                    subject=_("Redefinição de senha - {tenant}").format(tenant=tenant.name),
                    to_email=user.email,
                    template_name="password_reset/password_reset.html",
                    context=context,
                )
            except TemplateDoesNotExist:
                logger.warning("Template de e-mail de reset ausente; seguindo sem enviar HTML.")
            except Exception as e:
                logger.exception("Falha ao enviar e-mail de reset: %s", e)
        except User.DoesNotExist:
            pass  # Blind response

class PasswordResetConfirmSerializer(serializers.Serializer):
    params = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        # Decodifica parâmetros da URL
        try:
            params = decode_b64url(data["params"])
        except Exception:
            raise serializers.ValidationError(_("Parâmetros de redefinição inválidos."))

        email = params.get("email")
        schema_name = params.get("tenant")
        token = params.get("token")
        if not all([email, schema_name, token]):
            raise serializers.ValidationError(_("Parâmetros ausentes."))

        try:
            tenant = Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            raise serializers.ValidationError(_("Tenant inválido."))

        # Entra no contexto do schema correto
        with schema_context(schema_name):
            try:
                user = User.objects.get(email=email, tenant=tenant)
            except User.DoesNotExist:
                raise serializers.ValidationError(_("Usuário ou token inválido."))
            if not password_reset_token_generator.check_token(user, token):
                raise serializers.ValidationError(_("Token inválido ou expirado."))

        data['user'] = user
        data['tenant'] = tenant
        return data

    def save(self):
        user = self.validated_data['user']
        tenant = self.validated_data['tenant']
        new_password = self.validated_data['new_password']

        with schema_context(tenant.schema_name):
            user.set_password(new_password)
            user.save()
