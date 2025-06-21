# core/views.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from core.serializers import RegisterTenantSerializer

# Base ViewSet with tenant filtering (assuming TenantMainMiddleware sets request.tenant)
# This should be inherited by ViewSets in tenant-specific apps.
class TenantAwareViewSet(viewsets.ModelViewSet):
    """
    A base ModelViewSet that ensures operations are implicitly scoped
    to the current tenant managed by django-tenant-schemas.
    Assumes the model is part of TENANT_APPS and TenantMainMiddleware is active.
    """
    permission_classes = [permissions.IsAuthenticated] # Add specific tenant permissions later if needed
    filter_backends = [DjangoFilterBackend] # Enable filtering by default

    # No need to override get_queryset or perform_create for tenant filtering
    # if using django-tenant-schemas correctly with models in TENANT_APPS.
    # The middleware handles setting the schema context, and Django's ORM
    # automatically filters based on the current schema.

    # If you were using a single-schema approach with an explicit tenant_id ForeignKey:
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated and hasattr(user, 'tenant') and user.tenant:
    #         # Ensure the queryset attribute is defined in the subclass
    #         if hasattr(self, 'queryset'):
    #             return self.queryset.filter(tenant=user.tenant)
    #         else:
    #             # Fallback or raise error if queryset is not defined
    #             return self.model.objects.none() # Or self.get_serializer().Meta.model.objects.none()
    #     return self.model.objects.none() # Or self.get_serializer().Meta.model.objects.none()

    # def perform_create(self, serializer):
    #     # Automatically associate with the current tenant if model has explicit tenant field
    #     if hasattr(serializer.Meta.model, 'tenant'):
    #        serializer.save(tenant=self.request.user.tenant)
    #     else:
    #        # This case should ideally not happen for tenant-aware models
    #        serializer.save()

# Add other core views here if needed, e.g., for tenant registration
from rest_framework import generics
from .serializers import RegisterTenantSerializer
from .models import Tenant, Domain

class RegisterTenantView(generics.CreateAPIView):
    serializer_class = RegisterTenantSerializer
    permission_classes = [permissions.AllowAny] # Allow anyone to register a new tenant
    
    def perform_create(self, serializer):
        # The serializer's create method handles tenant, domain, and user creation
        serializer.save()


