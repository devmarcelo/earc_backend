from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, views, throttling
from core.handlers.response import success_response, error_response
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetRequestView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.")
        return error_response(errors=serializer.errors, message="Erro ao solicitar redefinição de senha.")

@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetConfirmView(views.APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [throttling.AnonRateThrottle]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return success_response(message="Senha redefinida com sucesso.")
        return error_response(errors=serializer.errors, message="Erro ao redefinir senha.")
