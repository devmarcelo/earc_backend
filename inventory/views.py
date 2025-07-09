from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, StockMovement, InventoryCount
from .serializers import ProductSerializer, StockMovementSerializer, InventoryCountSerializer
from core.views import TenantAwareViewSet

class ProductViewSet(TenantAwareViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = {
        "name": ["exact", "icontains"],
        "sku": ["exact"],
        "unit": ["exact"],
        "cost_price": ["exact", "gte", "lte"],
        "sale_price": ["exact", "gte", "lte"],
        "minimum_stock": ["exact", "gte", "lte"],
        "current_stock": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["name", "sku", "description"]

class StockMovementViewSet(TenantAwareViewSet):
    queryset = StockMovement.objects.select_related("product")
    serializer_class = StockMovementSerializer
    filterset_fields = {
        "product": ["exact"],
        "movement_type": ["exact"],
        "date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["product__name", "reference", "notes"]

class InventoryCountViewSet(TenantAwareViewSet):
    queryset = InventoryCount.objects.select_related("product")
    serializer_class = InventoryCountSerializer
    filterset_fields = {
        "product": ["exact"],
        "date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["product__name", "notes"]
