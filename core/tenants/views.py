from rest_framework import generics
from django.shortcuts import get_object_or_404
from django_tenants.utils import schema_context
from core.models import Tenant
from core.permissions import AllowOnlyGet
from .serializers import PublicTenantSettingsSerializer

class PublicTenantSettingsView(generics.RetrieveAPIView):
    queryset = Tenant.objects.filter(is_active=True, is_anonymized=False)
    serializer_class = PublicTenantSettingsSerializer
    permission_classes = [AllowOnlyGet]
    lookup_field = "schema_name"

    def get_object(self):
        # Protege contra injection/maus usos
        slug = self.kwargs.get("slug")
        with schema_context("public"):
            return get_object_or_404(Tenant.objects.filter(is_active=True, is_anonymized=False), schema_name=slug)
