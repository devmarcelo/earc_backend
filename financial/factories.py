# financial/factories.py
import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from .models import Cliente, Fornecedor, ContaPagarReceber, Despesa, Receita
from core.factories import TenantFactory, CategoriaFactory, UserFactory # Assuming UserFactory is needed for created_by

class ClienteFactory(DjangoModelFactory):
    class Meta:
        model = Cliente
        # Ensure tenant context is set before creating

    nome = factory.Faker("company")
    contato = factory.Faker("phone_number")
    endereco = factory.Faker("address")
    # tenant = factory.SubFactory(TenantFactory) # Tenant is set via context or view

class FornecedorFactory(DjangoModelFactory):
    class Meta:
        model = Fornecedor

    nome = factory.Faker("company")
    contato = factory.Faker("phone_number")
    cnpj = factory.Faker("numerify", text="##.###.###/####-##")
    # tenant = factory.SubFactory(TenantFactory)

class ContaPagarReceberFactory(DjangoModelFactory):
    class Meta:
        model = ContaPagarReceber

    descricao = factory.Faker("sentence", nb_words=4)
    valor = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    data_vencimento = factory.Faker("future_date", end_date="+60d")
    data_pagamento = factory.Maybe(
        "status",
        yes_declaration=factory.Faker("past_date", start_date="-30d"),
        no_declaration=None
    )
    status = factory.Iterator(["Pendente", "Pago", "Atrasado"])
    tipo = factory.Iterator(["Pagar", "Receber"]) # Pagar ou Receber
    cliente = factory.Maybe(
        "tipo",
        yes_declaration=factory.SubFactory(ClienteFactory),
        no_declaration=None
    )
    fornecedor = factory.Maybe(
        "tipo",
        yes_declaration=None,
        no_declaration=factory.SubFactory(FornecedorFactory)
    )
    # tenant = factory.SubFactory(TenantFactory)

class DespesaFactory(DjangoModelFactory):
    class Meta:
        model = Despesa

    descricao = factory.Faker("sentence", nb_words=3)
    valor = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    data = factory.Faker("past_date", start_date="-90d")
    categoria = factory.SubFactory(CategoriaFactory, tipo="D")
    fornecedor = factory.SubFactory(FornecedorFactory)
    # tenant = factory.SubFactory(TenantFactory)

class ReceitaFactory(DjangoModelFactory):
    class Meta:
        model = Receita

    descricao = factory.Faker("sentence", nb_words=3)
    valor = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    data = factory.Faker("past_date", start_date="-90d")
    categoria = factory.SubFactory(CategoriaFactory, tipo="R")
    cliente = factory.SubFactory(ClienteFactory)
    # tenant = factory.SubFactory(TenantFactory)
