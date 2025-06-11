# hr/views.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Funcionario
from .serializers import FuncionarioSerializer
# Ensure the import points to the correct location
from core.views import TenantAwareViewSet 

class FuncionarioViewSet(TenantAwareViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    filterset_fields = {
        "cargo": ["exact", "icontains"],
        "salario_base": ["exact", "gte", "lte"],
        "data_proximo_pagamento": ["exact", "gte", "lte"],
    }
    search_fields = ["nome", "cargo"]

