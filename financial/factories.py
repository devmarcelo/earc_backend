"""
FACTORIES DISABLED
------------------

This file is a legacy from a previous data model.
All factories below reference models, fields and business logic that no longer exist in the current project structure.

When implementing tests in the future, rewrite these factories in English, using the new models:
    - Customer
    - Supplier
    - Category
    - BankAccount
    - Expense
    - Revenue
    - Transfer

Example structure for Factory Boy:

# import factory
# from factory.django import DjangoModelFactory
# from financial.models import Customer, Supplier, Category, BankAccount, Expense, Revenue, Transfer

# class CustomerFactory(DjangoModelFactory):
#     class Meta:
#         model = Customer
#     name = factory.Faker("company")
#     document = factory.Faker("bothify", text="###.###.###-##")
#     ...

# Add new factories here as needed for future tests/seeding

---------------------
LEGACY CODE BELOW (do not use)
---------------------
"""

# Conteúdo legado comentado:
# import factory
# from factory.django import DjangoModelFactory
# from decimal import Decimal
# from .models import Cliente, Fornecedor, ContaPagarReceber, Despesa, Receita
# from core.factories import TenantFactory, CategoriaFactory, UserFactory

# class ClienteFactory(DjangoModelFactory):
#     ...
# class FornecedorFactory(DjangoModelFactory):
#     ...
# class ContaPagarReceberFactory(DjangoModelFactory):
#     ...
# class DespesaFactory(DjangoModelFactory):
#     ...
# class ReceitaFactory(DjangoModelFactory):
#     ...
