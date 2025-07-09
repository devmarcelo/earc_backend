"""
FACTORIES DISABLED
------------------

This file is a legacy from a previous HR model.
All factories below reference models and fields in Portuguese that no longer exist.

When implementing tests in the future, rewrite these factories in English, using the new models:
    - Employee
    - Payroll
    - Attendance

Example structure for Factory Boy:

# import factory
# from factory.django import DjangoModelFactory
# from hr.models import Employee, Payroll, Attendance

# class EmployeeFactory(DjangoModelFactory):
#     class Meta:
#         model = Employee
#     name = factory.Faker("name")
#     document = factory.Faker("bothify", text="###.###.###-##")
#     email = factory.Faker("email")
#     job_title = factory.Faker("job")
#     hire_date = factory.Faker("past_date", start_date="-3y")
#     base_salary = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True, min_value=1500)
#     tenant = factory.SubFactory(TenantFactory)

---------------------
LEGACY CODE BELOW (do not use)
---------------------
"""

# import factory
# from factory.django import DjangoModelFactory
# from decimal import Decimal
# from .models import Funcionario
# from core.factories import TenantFactory

# class FuncionarioFactory(DjangoModelFactory):
#     class Meta:
#         model = Funcionario
#     nome = factory.Faker("name")
#     cargo = factory.Faker("job")
#     data_contratacao = factory.Faker("past_date", start_date="-3y")
#     salario = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True, min_value=1500)
#     email = factory.Faker("email")
#     # tenant = factory.SubFactory(TenantFactory)
