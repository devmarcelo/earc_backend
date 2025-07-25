from rest_framework import generics, status
from core.models import Tenant
from core.permissions import AllowOnlyGet
from .serializers import PublicTenantSettingsSerializer
from django.utils.translation import gettext_lazy as _
from core.handlers.response import error_response, success_response
import traceback

class PublicTenantSettingsView(generics.RetrieveAPIView):
    """
    Endpoint público que retorna o branding de empresas cadastradas no sistema.
    """
    queryset = Tenant.objects.filter(is_active=True, is_anonymized=False)
    serializer_class = PublicTenantSettingsSerializer
    permission_classes = [AllowOnlyGet]
    lookup_field = "schema_name"

    def get(self, request, slug, *args, **kwargs):
        trace_id = getattr(request, "request_id", None)

        try:
            tenant = Tenant.objects.filter(is_active=True, is_anonymized=False, schema_name=slug).first()

            if not tenant:
                return error_response(
                    errors=[],
                    message=_("Empresa não encontrada ou inativa."),
                    status=status.HTTP_404_NOT_FOUND,
                    code="TENANT_NOT_FOUND",
                    trace_id=trace_id,
                )
            
            serializer = PublicTenantSettingsSerializer(tenant, context={"request": request})

            return success_response(
                message=_("Empresa encontrada"),
                status=status.HTTP_200_OK,
                data=serializer.data,
                trace_id=trace_id
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
            return error_response(
                errors=[str(e)],
                message=_("Dados inválidos."),
                status=status.HTTP_400_BAD_REQUEST,
                code="TENANT_BAD_REQUEST",
                trace_id=trace_id,
            )

