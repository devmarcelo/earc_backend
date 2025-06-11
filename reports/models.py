# reports/models.py
from django.db import models
from core.models import TenantAwareModel
from django.utils import timezone

class MetaResultado(TenantAwareModel):
    mes_ano = models.DateField(help_text="Primeiro dia do mês/ano da meta")
    meta_receita = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    receita_real = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Calculado/atualizado periodicamente ou via trigger")
    meta_lucro = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    lucro_real = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Calculado/atualizado periodicamente ou via trigger")
    # tenant field is implicit

    class Meta:
        verbose_name = "Meta e Resultado"
        verbose_name_plural = "Metas e Resultados"
        ordering = ["-mes_ano"]
        # Ensure unique goal per month/year within a tenant
        # unique_together = (("tenant", "mes_ano"),) # Requires explicit tenant field

    def __str__(self):
        return f"Metas {self.mes_ano.strftime('%Y-%m')}"

class ProjecaoCaixa(TenantAwareModel):
    data = models.DateField()
    entradas_previstas = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saidas_previstas = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # tenant field is implicit

    class Meta:
        verbose_name = "Projeção de Caixa"
        verbose_name_plural = "Projeções de Caixa"
        ordering = ["data"]
        # Ensure unique projection per day within a tenant
        # unique_together = (("tenant", "data"),) # Requires explicit tenant field

    def __str__(self):
        return f"Projeção {self.data}"

    @property
    def saldo_projetado_dia(self):
        """Calculates the projected balance change for the day."""
        return self.entradas_previstas - self.saidas_previstas

