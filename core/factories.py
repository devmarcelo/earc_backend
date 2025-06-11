# core/factories.py
import factory
from factory.django import DjangoModelFactory
from .models import Tenant, Domain, User, Categoria
from django.contrib.auth.hashers import make_password

class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant
        django_get_or_create = (
            "schema_name",
        ) # Use schema_name to find existing tenants

    schema_name = factory.LazyAttribute(lambda o: f"tenant_{o.name.lower().replace(' ', '')}")
    name = factory.Faker("company")
    # paid_until = factory.Faker("future_date", end_date="+30d")
    # on_trial = False

class DomainFactory(DjangoModelFactory):
    class Meta:
        model = Domain

    domain = factory.LazyAttribute(lambda o: f"{o.tenant.schema_name}.localhost") # Use .localhost for dev
    tenant = factory.SubFactory(TenantFactory)
    is_primary = True

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            "email",
        )

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("password"))
    is_active = True
    is_staff = False
    is_superuser = False
    tenant = factory.SubFactory(TenantFactory) # Associate user with a tenant

class CategoriaFactory(DjangoModelFactory):
    class Meta:
        model = Categoria
        django_get_or_create = (
            "nome",
        )

    nome = factory.Iterator(["Receita Venda", "Despesa Aluguel", "Despesa Salário", "Custo Mercadoria"])
    tipo = factory.Iterator(["R", "D", "D", "D"])
    # tenant = factory.SubFactory(TenantFactory) # Categoria is shared in this design
