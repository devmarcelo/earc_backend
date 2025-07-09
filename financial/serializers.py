from rest_framework import serializers
from .models import (
    Customer, Supplier, Category, BankAccount, Expense, Revenue, Transfer
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'document', 'email', 'phone', 'notes',
            'is_active', 'is_anonymized',
            'created_on', 'updated_on', 'created_by', 'updated_by',
            'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'document', 'email', 'phone', 'notes',
            'is_active', 'is_anonymized',
            'created_on', 'updated_on', 'created_by', 'updated_by',
            'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description',
            'is_active',
            'created_on', 'updated_on', 'created_by', 'updated_by', 'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            'id', 'name', 'bank', 'branch', 'account_number',
            'initial_balance', 'current_balance',
            'is_active',
            'created_on', 'updated_on', 'created_by', 'updated_by', 'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id', 'category', 'supplier', 'amount', 'date', 'description', 'paid', 'account', 'document',
            'is_active', 'is_anonymized',
            'created_on', 'updated_on', 'created_by', 'updated_by', 'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = [
            'id', 'category', 'customer', 'amount', 'date', 'description', 'received', 'account', 'document',
            'is_active', 'is_anonymized',
            'created_on', 'updated_on', 'created_by', 'updated_by', 'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            'id', 'source_account', 'destination_account', 'amount', 'date', 'description',
            'is_active',
            'created_on', 'updated_on', 'created_by', 'updated_by', 'tenant'
        ]
        read_only_fields = ('created_on', 'updated_on', 'created_by', 'updated_by', 'tenant')
