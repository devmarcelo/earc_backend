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
    Middleware centralizador: logging, validação, padronização de resposta e erros para toda a aplicação.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            result = self.process_request(request)
            if result is not None:
                return result
            response = self.get_response(request)
            return self.process_response(request, response)
        except Exception as exc:
            return self.process_exception(request, exc)

    def process_request(self, request):
        try:
            handle_request(request)
        except APIException as exc:
            return error_response(
                errors={exc.get_codes(): [exc.detail]},
                message=str(exc.detail),
                status=exc.status_code,
                code=exc.get_codes()
            )

    def process_exception(self, request, exception):
        from django.http import Http404
        trace_id = getattr(request, "request_id", None)
        if isinstance(exception, Http404):
            return error_response(
                errors={"detail": ["Endpoint não encontrado."]},
                message="Recurso não encontrado.",
                status=404,
                code="not_found",
                trace_id=trace_id
            )
        if isinstance(exception, APIException):
            return error_response(
                errors={exception.get_codes(): [exception.detail]},
                message=str(exception.detail),
                status=exception.status_code,
                code=exception.get_codes(),
                trace_id=trace_id
            )
        # Erros inesperados
        return error_response(
            errors={"detail": [str(exception)]},
            message="Erro interno do servidor.",
            status=500,
            code="internal_server_error",
            trace_id=trace_id
        )

    def process_response(self, request, response):
        trace_id = getattr(request, "request_id", None)
        if isinstance(response, Response):
            if isinstance(response.data, dict) and "success" in response.data and "message" in response.data:
                response.data["trace_id"] = trace_id
                return response
            if response.status_code >= 400:
                return error_response(
                    errors=response.data,
                    message="Erro ao processar requisição.",
                    status=response.status_code,
                    trace_id=trace_id
                )
            return success_response(
                message="Operação realizada com sucesso.",
                data=response.data,
                status=response.status_code,
                trace_id=trace_id
            )
        return response