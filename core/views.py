# core/views.py
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.db import connection
from ai.events import emit_event
from core.security.throttles import LoginRateThrottle
from .serializers import RegisterTenantSerializer, LoginSerializer, TenantSerializer
from core.handlers.response import success_response, error_response
from core.utils.security import register_token_attempt, is_token_blocked
from django.utils.translation import gettext_lazy as _
import traceback

# Base ViewSet with tenant filtering (assuming TenantMainMiddleware sets request.tenant)
# This should be inherited by ViewSets in tenant-specific apps.
class TenantAwareViewSet(viewsets.ModelViewSet):
    """
    A base ModelViewSet that ensures operations are implicitly scoped
    to the current tenant managed by django-tenant-schemas.
    Assumes the model is part of TENANT_APPS and TenantMainMiddleware is active.
    """
    permission_classes = [permissions.IsAuthenticated] # Add specific tenant permissions later if needed
    filter_backends = [DjangoFilterBackend] # Enable filtering by default

    # No need to override get_queryset or perform_create for tenant filtering
    # if using django-tenant-schemas correctly with models in TENANT_APPS.
    # The middleware handles setting the schema context, and Django's ORM
    # automatically filters based on the current schema.

    # If you were using a single-schema approach with an explicit tenant_id ForeignKey:
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated and hasattr(user, 'tenant') and user.tenant:
    #         # Ensure the queryset attribute is defined in the subclass
    #         if hasattr(self, 'queryset'):
    #             return self.queryset.filter(tenant=user.tenant)
    #         else:
    #             # Fallback or raise error if queryset is not defined
    #             return self.model.objects.none() # Or self.get_serializer().Meta.model.objects.none()
    #     return self.model.objects.none() # Or self.get_serializer().Meta.model.objects.none()

    # def perform_create(self, serializer):
    #     # Automatically associate with the current tenant if model has explicit tenant field
    #     if hasattr(serializer.Meta.model, 'tenant'):
    #        serializer.save(tenant=self.request.user.tenant)
    #     else:
    #        # This case should ideally not happen for tenant-aware models
    #        serializer.save()

# Add other core views here if needed, e.g., for tenant registration

class RegisterTenantView(generics.CreateAPIView):
    serializer_class = RegisterTenantSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save()
        trace_id = getattr(request, "request_id", None)
        data = TenantSerializer(tenant).data
        headers = self.get_success_headers(data)
        return success_response(
            data=data,
            message="Empresa criada com sucesso.",
            trace_id=trace_id,
            status=status.HTTP_201_CREATED
        )
    
    def perform_create(self, serializer):
        serializer.save()

class LoginView(generics.GenericAPIView):
    """
    Login seguro, multi-tenant, JWT.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        trace_id = getattr(request, "request_id", None)
        tenant = getattr(request, "tenant", None)
        serializer = self.get_serializer(data=request.data, context={"request": request})

        if not tenant or tenant.schema_name == "public":
            return error_response(
                message=_("Tenant não identificado. Verifique o domínio/subdomínio da requisição."),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if not serializer.is_valid():
                return error_response(
                    message=_("Dados inválidos."),
                    errors=serializer.errors,
                    trace_id=trace_id,
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = serializer.validated_data["user"]
            tenant = serializer.validated_data["tenant"]

            # Exemplo de logging/auditoria para brute-force (pode expandir com model ou Redis)
            # register_login_attempt(email, tenant=request.tenant, success=False)
            
            # Tudo OK, logar sucesso
            # register_login_attempt(email, tenant=request.tenant, success=True)

            refresh = RefreshToken.for_user(user)

            user_data = {
                "id": user.id,
                "email": user.email,
                "name": user.get_full_name(),
            }

            tenant_data = TenantSerializer(tenant).data

            emit_event(
                "auth.login.success", 
                {"user_id": user.id, "email": user.email}, 
                tenant_schema=connection.schema_name, 
                source="api"
            )

            return success_response(
                data={
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": user_data,
                    "tenant": tenant_data
                },
                message=_("Login realizado com sucesso."),
                trace_id=trace_id,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            traceback.print_exc()
            return error_response(
                errors=serializer.errors,
                message=str(e),
                trace_id=trace_id,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TokenRefreshView(APIView):
    """
    Endpoint robusto para refresh de JWT, com validações extras de tenant,
    limite de tentativas e resposta padronizada.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        trace_id = request.META.get("TRACE_ID") or ""
        tenant = getattr(request, "tenant", None)
        data = request.data.copy()

        refresh_token = data.get("refresh")
        if is_token_blocked(refresh_token, tenant):
            return error_response(
                message=_("Token bloqueado por tentativas inválidas."),
                code="token_blocked",
                status=status.HTTP_403_FORBIDDEN,
                trace_id=trace_id
            )

        serializer = TokenRefreshSerializer(data=data)
        if not serializer.is_valid():
            register_token_attempt(refresh_token, tenant, success=False)
            return error_response(
                message=_("Refresh token inválido ou expirado."),
                errors=serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED,
                trace_id=trace_id
            )

        # 3. Verificação de tenant/contexto, se necessário (custom)
        # Exemplo: checar se o refresh pertence a esse tenant
        # (Customização depende de como o tenant está associado ao user/token)

        register_token_attempt(refresh_token, tenant, success=True)
        return success_response(
            message=_("Token atualizado com sucesso."),
            data=serializer.validated_data,
            trace_id=trace_id,
            status=status.HTTP_200_OK,
            request=request
        )
