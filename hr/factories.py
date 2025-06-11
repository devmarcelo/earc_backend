# hr/factories.py
import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from .models import Funcionario
from core.factories import TenantFactory # Assuming tenant is set via context

class FuncionarioFactory(DjangoModelFactory):
    class Meta:
        model = Funcionario

    nome = factory.Faker("name")
    cargo = factory.Faker("job")
    data_contratacao = factory.Faker("past_date", start_date="-3y")
    salario = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True, min_value=1500)
    email = factory.Faker("email")
    # tenant = factory.SubFactory(TenantFactory) # Tenant is set via context or view

