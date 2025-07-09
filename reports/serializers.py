from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = Report
        fields = [
            "id", "name", "description", "report_type", "parameters",
            "file_url", "generated_at", "is_active", "is_anonymized",
            "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = [
            "id", "file_url", "generated_at", "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]

# --- Serializers for Report Generation (Read-only) ---

class FinancialSummarySerializer(serializers.Serializer):
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    net_profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    profit_margin_percent = serializers.FloatField(read_only=True)
    target_profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    target_achieved_percent = serializers.FloatField(read_only=True, allow_null=True)
    open_accounts_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_inventory_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class CashFlowEntrySerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    inflow = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    outflow = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    daily_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class CashFlowReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    initial_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    entries = CashFlowEntrySerializer(many=True, read_only=True)
    final_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class ExpenseByCategoryEntrySerializer(serializers.Serializer):
    category_id = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(read_only=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class ExpenseByCategoryReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    entries = ExpenseByCategoryEntrySerializer(many=True, read_only=True)
