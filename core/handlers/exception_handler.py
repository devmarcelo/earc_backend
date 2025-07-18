from rest_framework.views import exception_handler
import logging

try:
    import sentry_sdk
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

logger = logging.getLogger("core.security")

def custom_exception_handler(exc, context):
    """
    Custom handler:
    - Padroniza resposta de erro.
    - Adiciona trace_id.
    - Envia exceções críticas ao Sentry se configurado.
    - Loga warnings/erros relevantes.
    """
    response = exception_handler(exc, context)
    request = context.get('request') if context else None
    trace_id = getattr(request, 'request_id', None) if request else None

    # Opcional: capture no Sentry só se for erro server-side (500+) ou erro crítico
    should_report = (
        response is None or
        (response is not None and getattr(response, 'status_code', 500) >= 500)
    )
    if HAS_SENTRY and should_report:
        sentry_sdk.capture_exception(exc)

    # Logging local para debugging/auditoria
    logger.warning(
        f"Exception handled | TraceID={trace_id} | Path={getattr(request, 'path', None)} | Exc={exc.__class__.__name__}: {exc}"
    )

    # Padroniza resposta
    if response is not None:
        data = response.data
        response.data = {
            "success": False,
            "message": "Erro ao processar requisição.",
            "errors": data,
            "trace_id": trace_id,
        }
    else:
        # Se não houve response DRF (erro crítico), retorna erro padronizado
        from rest_framework.response import Response
        response = Response(
            {
                "success": False,
                "message": "Erro interno do servidor.",
                "errors": str(exc),
                "trace_id": trace_id,
            },
            status=500
        )

    return response
