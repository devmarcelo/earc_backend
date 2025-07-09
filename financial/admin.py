from django.contrib import admin
from .models import (
    Customer, Supplier, Category, BankAccount, Expense, Revenue, Transfer
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "document", "email", "phone", "tenant", "is_active", "created_on")
    search_fields = ("name", "document", "email", "phone")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "document", "email", "phone", "tenant", "is_active", "created_on")
    search_fields = ("name", "document", "email", "phone")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "tenant", "is_active", "created_on")
    search_fields = ("name",)
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on")

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "bank", "branch", "account_number", "tenant", "is_active", "created_on")
    search_fields = ("name", "bank", "branch", "account_number")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "date", "paid", "supplier", "account", "tenant", "is_active", "created_on")
    search_fields = ("category__name", "supplier__name", "account__name", "document")
    list_filter = ("tenant", "category", "paid", "is_active", "date")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "date", "received", "customer", "account", "tenant", "is_active", "created_on")
    search_fields = ("category__name", "customer__name", "account__name", "document")
    list_filter = ("tenant", "category", "received", "is_active", "date")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("source_account", "destination_account", "amount", "date", "tenant", "is_active", "created_on")
    search_fields = ("source_account__name", "destination_account__name")
    list_filter = ("tenant", "is_active", "date")
    readonly_fields = ("tenant", "created_on", "updated_on")
