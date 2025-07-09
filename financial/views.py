from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Customer, Supplier, Category, BankAccount, Expense, Revenue, Transfer
)
from .serializers import (
    CustomerSerializer, SupplierSerializer, CategorySerializer,
    BankAccountSerializer, ExpenseSerializer, RevenueSerializer, TransferSerializer
)
from core.views import TenantAwareViewSet

class CustomerViewSet(TenantAwareViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ["name", "document", "email", "phone", "is_active"]
    search_fields = ["name", "document", "email", "phone", "notes"]
    permission_classes = [permissions.IsAuthenticated]

class SupplierViewSet(TenantAwareViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ["name", "document", "email", "phone", "is_active"]
    search_fields = ["name", "document", "email", "phone", "notes"]
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(TenantAwareViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ["name", "is_active"]
    search_fields = ["name", "description"]
    permission_classes = [permissions.IsAuthenticated]

class BankAccountViewSet(TenantAwareViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    filterset_fields = ["name", "bank", "branch", "account_number", "is_active"]
    search_fields = ["name", "bank", "branch", "account_number"]
    permission_classes = [permissions.IsAuthenticated]

class ExpenseViewSet(TenantAwareViewSet):
    queryset = Expense.objects.select_related("category", "supplier", "account")
    serializer_class = ExpenseSerializer
    filterset_fields = ["category", "supplier", "account", "paid", "date", "is_active"]
    search_fields = ["description", "document", "supplier__name", "category__name"]
    permission_classes = [permissions.IsAuthenticated]

class RevenueViewSet(TenantAwareViewSet):
    queryset = Revenue.objects.select_related("category", "customer", "account")
    serializer_class = RevenueSerializer
    filterset_fields = ["category", "customer", "account", "received", "date", "is_active"]
    search_fields = ["description", "document", "customer__name", "category__name"]
    permission_classes = [permissions.IsAuthenticated]

class TransferViewSet(TenantAwareViewSet):
    queryset = Transfer.objects.select_related("source_account", "destination_account")
    serializer_class = TransferSerializer
    filterset_fields = ["source_account", "destination_account", "date", "is_active"]
    search_fields = ["description", "source_account__name", "destination_account__name"]
    permission_classes = [permissions.IsAuthenticated]
