from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    trace_id = getattr(context['request'], 'request_id', None)
    if response is not None:
        data = response.data
        response.data = {
            "success": False,
            "message": "Erro ao processar requisição.",
            "errors": data,
            "trace_id": trace_id,
        }
    return response
