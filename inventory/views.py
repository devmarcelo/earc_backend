# inventory/views.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import ItemEstoque
from .serializers import ItemEstoqueSerializer
# Ensure the import points to the correct location
from core.views import TenantAwareViewSet 

class ItemEstoqueViewSet(TenantAwareViewSet):
    queryset = ItemEstoque.objects.all().select_related("categoria") # Optimize query
    serializer_class = ItemEstoqueSerializer
    filterset_fields = {
        "quantidade": ["exact", "gte", "lte"],
        "custo_unitario": ["exact", "gte", "lte"],
        "categoria": ["exact"],
    }
    search_fields = ["nome_produto", "categoria__nome"]

