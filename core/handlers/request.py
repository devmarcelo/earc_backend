import uuid
import logging
from django.conf import settings
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

try:
    import sentry_sdk
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

logger = logging.getLogger("core.request")

def handle_request(request):
    # Gera request_id para rastreamento/logging
    trace_id = getattr(request, "request_id", None)
    if not trace_id:
        trace_id = str(uuid.uuid4())
        request.request_id = trace_id

    # Se Sentry estiver ativo, adiciona o trace_id no escopo
    if HAS_SENTRY:
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("trace_id", trace_id)

    # --- Logging da requisição ---
    logger.info(
        f"REQUEST | ID={trace_id} | PATH={getattr(request, "path", "")} | METHOD={getattr(request, "method", "")} | USER={getattr(request.user, "email", "anon")}"
    )

    # --- Validação de headers obrigatórios para APIs públicas/integradas ---
    # Exemplo: API Key obrigatória para endpoints públicos ou integrações
    if getattr(settings, "REQUIRE_API_KEY", False):
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != getattr(settings, "API_KEY_VALUE", None):
            logger.warning(f"REQUEST BLOCKED | ID={trace_id} | Motivo=API Key missing/invalid")
            raise PermissionDenied(detail="API Key obrigatória ou inválida.")

    # --- Quotas (simples): limite de requisições por IP/hora (exemplo simplificado) ---
    # Pode ser substituído por solução avançada tipo Django Ratelimit ou Redis
    if getattr(settings, "ENABLE_BASIC_QUOTA", False):
        ip = request.META.get("REMOTE_ADDR")
        # Exemplo didático; produção exige cache/Redis para rastrear IPs
        if hasattr(request, "quota_checked"):  # skip in tests
            pass
        # else: verificar quota no Redis/cache e levantar exceção se necessário

    # --- Validação de tenant_id (para endpoints multi-tenant públicos) ---
    if getattr(settings, "REQUIRE_TENANT_HEADER", False):
        tenant_id = request.headers.get("X-TENANT-ID")
        if not tenant_id:
            logger.warning(f"REQUEST BLOCKED | ID={trace_id} | Motivo=Tenant ID missing")
            raise NotAuthenticated(detail="Tenant ID obrigatório para esta operação.")

    # Outras validações avançadas podem ser plugadas aqui (antifraude, analytics, partner-id, etc)
