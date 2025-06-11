# financial/models.py
from django.db import models
from core.models import TenantAwareModel, Categoria, User # Assuming User might be linked later, though not directly in these models

class Cliente(TenantAwareModel):
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    # tenant field is implicit

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Fornecedor(TenantAwareModel):
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=18, blank=True, null=True) # Format: XX.XXX.XXX/XXXX-XX
    # tenant field is implicit

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Receita(TenantAwareModel):
    data = models.DateField()
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="receitas")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="receitas", limit_choices_to={"tipo": "Receita"})
    # tenant field is implicit

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"

class Despesa(TenantAwareModel):
    data = models.DateField()
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="despesas")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="despesas", limit_choices_to={"tipo": "Despesa"})
    # tenant field is implicit

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"

class ContaPagarReceber(TenantAwareModel):
    TIPO_CHOICES = [
        ("Pagar", "A Pagar"),
        ("Receber", "A Receber"),
    ]
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Pago", "Pago"),
        ("Atrasado", "Atrasado"),
        ("Cancelado", "Cancelado"), # Added Cancelado status
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pendente")
    data_pagamento = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name="contas_receber")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="contas_pagar")
    # tenant field is implicit

    class Meta:
        verbose_name = "Conta a Pagar/Receber"
        verbose_name_plural = "Contas a Pagar/Receber"
        ordering = ["data_vencimento"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} - Venc: {self.data_vencimento} - Status: {self.get_status_display()}"

    # Add logic for status updates (e.g., in save method or via a separate service/task)
    # def save(self, *args, **kwargs):
    #     if not self.pk: # Check if new
    #         # Initial status logic if needed
    #         pass
    #     # Update status based on dates if needed (consider doing this in a service)
    #     super().save(*args, **kwargs)

