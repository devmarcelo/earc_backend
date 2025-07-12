import threading
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from core.handlers.request import handle_request
from core.handlers.response import success_response, error_response

_thread_locals = threading.local()

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
        response = self.get_response(request)
        return response

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
        # Continua o fluxo normalmente
        response = self.get_response(request)
        # Adiciona trace_id nos headers
        trace_id = getattr(request, "request_id", None)
        if trace_id:
            response['X-Trace-ID'] = trace_id
        return response