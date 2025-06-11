# inventory/factories.py
import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from .models import ItemEstoque
from core.factories import TenantFactory # Assuming tenant is set via context

class ItemEstoqueFactory(DjangoModelFactory):
    class Meta:
        model = ItemEstoque

    nome = factory.Faker("word")
    descricao = factory.Faker("sentence", nb_words=5)
    quantidade = factory.Faker("random_int", min=0, max=1000)
    preco_unitario = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    # tenant = factory.SubFactory(TenantFactory) # Tenant is set via context or view

