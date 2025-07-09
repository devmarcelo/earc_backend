from rest_framework import serializers
from .models import Product, StockMovement, InventoryCount

class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "sku", "description", "unit",
            "cost_price", "sale_price", "minimum_stock", "current_stock",
            "image", "is_active", "is_anonymized",
            "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]

class StockMovementSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            "id", "product", "quantity", "date", "movement_type",
            "reference", "notes", "is_active", "is_anonymized",
            "created_on", "updated_on", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "tenant_id", "product"
        ]

class InventoryCountSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = InventoryCount
        fields = [
            "id", "product", "counted_quantity", "date", "notes",
            "is_active", "is_anonymized", "created_on", "updated_on", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "tenant_id", "product"
        ]
