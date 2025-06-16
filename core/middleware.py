# core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from threading import local

_thread_locals = local()

def get_current_user():
    """
    Retorna o usuário atual da requisição armazenado no thread local.
    """
    return getattr(_thread_locals, 'user', None)

def get_current_tenant():
    """
    Retorna o tenant atual da requisição armazenado no thread local.
    """
    return getattr(_thread_locals, 'tenant', None)

class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware que armazena o usuário atual no thread local para acesso em qualquer parte do código.
    """
    def process_request(self, request):
        _thread_locals.user = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
        # Also store the tenant for audit purposes
        _thread_locals.tenant = getattr(request, 'tenant', None)

class RowLevelSecurityMiddleware(MiddlewareMixin):
    """
    Middleware para configurar variáveis de sessão do PostgreSQL para Row-Level Security (RLS).
    """
    def process_request(self, request):
        if hasattr(request, 'tenant') and request.tenant:
            # Define a variável de sessão do PostgreSQL para o tenant atual
            with connection.cursor() as cursor:
                cursor.execute("SET SESSION earc.current_tenant_id = %s", [request.tenant.id])
                
                # Se o usuário estiver autenticado, define a variável de sessão para o usuário atual
                if hasattr(request, 'user') and request.user.is_authenticated:
                    cursor.execute("SET SESSION earc.current_user_id = %s", [request.user.id])
                else:
                    cursor.execute("SET SESSION earc.current_user_id = NULL")
