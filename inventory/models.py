from django.db import models
from core.models import TenantAwareModel

class Product(TenantAwareModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=20, default="un")
    cost_price = models.DecimalField(max_digits=14, decimal_places=2)
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)
    minimum_stock = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_stock = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    image = models.URLField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        unique_together = (('tenant', 'sku'),)
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'sku']),
            models.Index(fields=['tenant', 'name']),
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def anonymize(self):
        self.name = ""
        self.description = ""
        self.sku = ""
        self.image = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name

class StockMovement(TenantAwareModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    quantity = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(
        max_length=20,
        choices=[("entry", "Entry"), ("exit", "Exit")]
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Reference number for NF-e, order, production, or other origin document."
    )
    notes = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'product']),
            models.Index(fields=['tenant', 'movement_type']),
            models.Index(fields=['tenant', 'reference']),
        ]
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'

    def anonymize(self):
        self.reference = ""
        self.notes = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return f"{self.product} - {self.movement_type} - {self.quantity}"

class InventoryCount(TenantAwareModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counted_quantity = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'product']),
            models.Index(fields=['tenant', 'date']),
        ]
        verbose_name = 'Inventory Count'
        verbose_name_plural = 'Inventory Counts'

    def anonymize(self):
        self.notes = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return f"{self.product} - {self.date} - {self.counted_quantity}"
