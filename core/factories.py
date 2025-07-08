"""
Factories for core app models.
To be used with Factory Boy for automated tests and data seeding.
Currently, models and fields are being refactored—update factories before using in tests.
"""

# import factory
# from factory.django import DjangoModelFactory
# from .models import Tenant, Domain, User
# from financial.models import Category
# from django.contrib.auth.hashers import make_password

# class TenantFactory(DjangoModelFactory):
#     class Meta:
#         model = Tenant
#     name = factory.Faker("company")
#     document = factory.Faker("bothify", text="##.###.###/####-##")
#     logo = factory.Faker("image_url")
#     is_active = True

# class DomainFactory(DjangoModelFactory):
#     class Meta:
#         model = Domain
#     domain = factory.LazyAttribute(lambda o: f"{o.tenant.name.lower().replace(' ', '')}.localhost")
#     tenant = factory.SubFactory(TenantFactory)
#     is_primary = True

# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User
#     first_name = factory.Faker("first_name")
#     last_name = factory.Faker("last_name")
#     email = factory.Faker("email")
#     password = factory.LazyFunction(lambda: make_password("password"))
#     is_active = True
#     is_staff = False
#     is_superuser = False
#     tenant = factory.SubFactory(TenantFactory)

# # class CategoryFactory(DjangoModelFactory):
# #     class Meta:
# #         model = Category
# #     name = factory.Iterator(["Sales Revenue", "Rent Expense", "Salary Expense", "Goods Cost"])
# #     type = factory.Iterator(["R", "E", "E", "E"])

# For usage examples, see: https://factoryboy.readthedocs.io/en/stable/
