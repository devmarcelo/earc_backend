# inventory/models.py
from django.db import models
from core.models import TenantAwareModel, Categoria

class ItemEstoque(TenantAwareModel):
    nome_produto = models.CharField(max_length=255)
    quantidade = models.IntegerField(default=0)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="itens_estoque", limit_choices_to={"tipo": "Estoque"})
    # tenant field is implicit

    class Meta:
        verbose_name = "Item de Estoque"
        verbose_name_plural = "Itens de Estoque"
        ordering = ["nome_produto"]

    def __str__(self):
        return self.nome_produto

    @property
    def valor_total(self):
        """Calculates the total value of this stock item."""
        return self.quantidade * self.custo_unitario

