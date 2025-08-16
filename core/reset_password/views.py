# core/reset_password/views.py
from django.db import connection
from ai.events import emit_event
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, views
from core.handlers.response import success_response, error_response
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

# throttling dedicado
try:
    from core.security.throttles import ResetRateThrottle
    _ResetThrottle = [ResetRateThrottle]
except Exception:
    from rest_framework import throttling
    _ResetThrottle = [throttling.AnonRateThrottle]

@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = _ResetThrottle

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            emit_event(
                "auth.password.reset.requested",
                {"email": serializer.validated_data.get("email")},
                tenant_schema=connection.schema_name,
                source="api"
            )

            return success_response(message="Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.")
        return error_response(errors=serializer.errors, message="Erro ao solicitar redefinição de senha.")

@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = _ResetThrottle

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            emit_event(
                "auth.password.reset.confirmed", 
                {"user_id": getattr(getattr(request, "user", None), "id", None)}, 
                tenant_schema=connection.schema_name, 
                source="api"
            )
            
            return success_response(message="Senha redefinida com sucesso.")
        return error_response(errors=serializer.errors, message="Erro ao redefinir senha.")
