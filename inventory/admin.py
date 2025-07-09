from django.contrib import admin
from .models import Product, StockMovement, InventoryCount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "current_stock", "unit", "cost_price", "sale_price", "is_active", "tenant", "created_on")
    search_fields = ("name", "sku")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "date", "reference", "tenant", "is_active", "created_on")
    search_fields = ("product__name", "reference", "notes")
    list_filter = ("tenant", "movement_type", "is_active", "date")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(InventoryCount)
class InventoryCountAdmin(admin.ModelAdmin):
    list_display = ("product", "counted_quantity", "date", "tenant", "is_active", "created_on")
    search_fields = ("product__name",)
    list_filter = ("tenant", "date", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")
