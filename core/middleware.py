import threading
import logging

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from core.handlers.request import handle_request

try:
    import sentry_sdk
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

_thread_locals = threading.local()
request_logger = logging.getLogger("core.request")

def get_current_user():
    """Return the current user from thread-local storage."""
    return getattr(_thread_locals, 'user', None)

def get_current_tenant():
    """Return the current tenant from thread-local storage."""
    return getattr(_thread_locals, 'tenant', None)

class CurrentUserTenantMiddleware:
    """
    Middleware to store the current user and tenant in thread-local storage.
    This allows other parts of the system (e.g., signals, audit) to access the current user and tenant safely within the request context.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.tenant = getattr(request, 'tenant', None)
        return self.get_response(request)

class RequestResponseCentralizerMiddleware:
    """
    Middleware centralizador: logging, rastreamento, validação da request (via handler), e headers.
    NUNCA manipula ou re-formata o body/response.data.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Valida e rastreia a request
        handle_request(request)
        trace_id = getattr(request, "request_id", None)

        if not trace_id:
            import uuid
            trace_id = str(uuid.uuid4())
            setattr(request, "request_id", trace_id)

        # Integra o trace_id ao contexto do Sentry (se ativado)
        if HAS_SENTRY:
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("trace_id", trace_id)
                if hasattr(request, 'user') and getattr(request.user, 'email', None):
                    scope.user = {"email": request.user.email}

        # Logging de início da request
        request_logger.info(
            f"START | TRACE_ID={trace_id} | PATH={request.path} | METHOD={request.method} | USER={getattr(request.user, 'email', 'anon')}"
        )

        response = self.get_response(request)

        if trace_id:
            response['X-Trace-ID'] = trace_id

        # Logging de fim da request
        request_logger.info(
            f"END | TRACE_ID={trace_id} | PATH={request.path} | STATUS={getattr(response, 'status_code', '?')}"
        )

        return response