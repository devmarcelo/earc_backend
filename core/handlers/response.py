import logging
from rest_framework.response import Response

try:
    import sentry_sdk
    HAS_SENTRY = True
except ImportError:
    HAS_SENTRY = False

logger = logging.getLogger("core.response")

def success_response(message, data=None, status=200, trace_id=None, meta=None, **kwargs):
    payload = {
        "success": True,
        "message": message,
        "data": data or {},
    }

    if trace_id:
        payload["trace_id"] = trace_id
    
    if meta:
        payload["meta"] = meta
    
    payload.update(kwargs)
    logger.info(f"RESPONSE | TRACE_ID={trace_id} | STATUS={status} | SUCCESS=True | MSG={message}")
    return Response(payload, status=status)

def error_response(errors, message=None, status=400, code=None, trace_id=None, meta=None, **kwargs):
    payload = {
        "success": False,
        "message": message or "Erro ao processar requisição.",
        "errors": errors,
    }

    if code:
        payload["code"] = code
    
    if trace_id:
        payload["trace_id"] = trace_id
    
    if meta:
        payload["meta"] = meta
    
    payload.update(kwargs)
    
    _err_str = str(errors)
    if len(_err_str) > 500:
        _err_str = _err_str[:500] + "... [truncated]"

    logger.warning(f"RESPONSE | TRACE_ID={trace_id} | STATUS={status} | SUCCESS=False | CODE={code} | ERRORS={_err_str}")

    if HAS_SENTRY and status >= 500:
        sentry_sdk.capture_message(
            f"Erro crítico na API | TRACE_ID={trace_id} | STATUS={status} | CODE={code} | MSG={message}",
            level="error"
        )

    return Response(payload, status=status)
