"""
FACTORIES DISABLED
------------------

This file is a legacy from a previous inventory model.
All factories below reference models and fields in Portuguese that no longer exist.

When implementing tests in the future, rewrite these factories in English, using the new models:
    - Product
    - StockMovement
    - InventoryCount

Example structure for Factory Boy:

# import factory
# from factory.django import DjangoModelFactory
# from inventory.models import Product, StockMovement, InventoryCount

# class ProductFactory(DjangoModelFactory):
#     class Meta:
#         model = Product
#     name = factory.Faker("word")
#     sku = factory.Faker("ean", length=8)
#     description = factory.Faker("sentence", nb_words=5)
#     current_stock = factory.Faker("random_int", min=0, max=1000)
#     cost_price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
#     sale_price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
#     tenant = factory.SubFactory(TenantFactory)

---------------------
LEGACY CODE BELOW (do not use)
---------------------
"""

# import factory
# from factory.django import DjangoModelFactory
# from decimal import Decimal
# from .models import ItemEstoque
# from core.factories import TenantFactory

# class ItemEstoqueFactory(DjangoModelFactory):
#     class Meta:
#         model = ItemEstoque
#     nome = factory.Faker("word")
#     descricao = factory.Faker("sentence", nb_words=5)
#     quantidade = factory.Faker("random_int", min=0, max=1000)
#     preco_unitario = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
#     # tenant = factory.SubFactory(TenantFactory)
