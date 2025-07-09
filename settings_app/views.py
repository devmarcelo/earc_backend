# settings_app/views.py

from rest_framework import viewsets, permissions
from .models import Parameter, Integration
from .serializers import ParameterSerializer, IntegrationSerializer
from core.views import TenantAwareViewSet

class ParameterViewSet(TenantAwareViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["key", "is_active"]
    search_fields = ["key", "value", "description"]

class IntegrationViewSet(TenantAwareViewSet):
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["service", "is_active"]
    search_fields = ["name", "service", "description"]
