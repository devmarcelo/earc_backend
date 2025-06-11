# hr/models.py
from django.db import models
from core.models import TenantAwareModel

class Funcionario(TenantAwareModel):
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    encargos_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentual de encargos sobre o salário base, ex: 25.00 para 25%")
    data_proximo_pagamento = models.DateField(null=True, blank=True)
    # tenant field is implicit

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    @property
    def custo_total_aproximado(self):
        """Calculates the approximate total cost (base salary + charges)."""
        if self.encargos_percentual is not None:
            encargos = self.salario_base * (self.encargos_percentual / 100)
            return self.salario_base + encargos
        return self.salario_base

