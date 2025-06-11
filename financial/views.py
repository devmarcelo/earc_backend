# financial/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, Fornecedor, Receita, Despesa, ContaPagarReceber
from .serializers import (
    ClienteSerializer, FornecedorSerializer, 
    ReceitaSerializer, DespesaSerializer, 
    ContaPagarReceberSerializer, MarkAsPaidSerializer
)
# Import the base viewset from core
from core.views import TenantAwareViewSet 
# Import custom permission if needed, e.g., IsTenantMember
# from core.permissions import IsTenantMember 

# REMOVED local definition of TenantAwareViewSet as it's now in core/views.py

class ClienteViewSet(TenantAwareViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_fields = ["nome", "contato"] # Fields to allow filtering on
    search_fields = ["nome", "contato", "endereco"] # Fields for search

class FornecedorViewSet(TenantAwareViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    filterset_fields = ["nome", "contato", "cnpj"]
    search_fields = ["nome", "contato", "cnpj"]

class ReceitaViewSet(TenantAwareViewSet):
    queryset = Receita.objects.all().select_related("cliente", "categoria") # Optimize query
    serializer_class = ReceitaSerializer
    filterset_fields = {
        "data": ["exact", "gte", "lte", "year", "month"],
        "valor": ["exact", "gte", "lte"],
        "cliente": ["exact"],
        "categoria": ["exact"],
    }
    search_fields = ["descricao", "cliente__nome", "categoria__nome"]

class DespesaViewSet(TenantAwareViewSet):
    queryset = Despesa.objects.all().select_related("fornecedor", "categoria") # Optimize query
    serializer_class = DespesaSerializer
    filterset_fields = {
        "data": ["exact", "gte", "lte", "year", "month"],
        "valor": ["exact", "gte", "lte"],
        "fornecedor": ["exact"],
        "categoria": ["exact"],
    }
    search_fields = ["descricao", "fornecedor__nome", "categoria__nome"]

class ContaPagarReceberViewSet(TenantAwareViewSet):
    queryset = ContaPagarReceber.objects.all().select_related("cliente", "fornecedor") # Optimize query
    serializer_class = ContaPagarReceberSerializer
    filterset_fields = {
        "tipo": ["exact"],
        "status": ["exact"],
        "data_vencimento": ["exact", "gte", "lte", "year", "month"],
        "data_pagamento": ["exact", "gte", "lte", "isnull"],
        "cliente": ["exact"],
        "fornecedor": ["exact"],
    }
    search_fields = ["descricao", "cliente__nome", "fornecedor__nome"]

    @action(detail=True, methods=["patch"], serializer_class=MarkAsPaidSerializer, url_path="mark-as-paid")
    def mark_as_paid(self, request, pk=None):
        """Custom action to mark an account as paid."""
        conta = self.get_object()
        if conta.status == "Pago":
            return Response({"detail": "Esta conta já foi marcada como paga."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(conta, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return the updated object using the main serializer
        updated_serializer = self.serializer_class(conta, context=self.get_serializer_context())
        return Response(updated_serializer.data)

