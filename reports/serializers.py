# reports/serializers.py
from rest_framework import serializers
from .models import MetaResultado, ProjecaoCaixa

class MetaResultadoSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    class Meta:
        model = MetaResultado
        fields = [
            "id", "mes_ano", "meta_receita", "receita_real", 
            "meta_lucro", "lucro_real", "created_on", "updated_at",
            "created_by", "updated_by", "tenant_id"
        ]
        # receita_real and lucro_real might be read-only if calculated by backend services
        read_only_fields = ["id", "receita_real", "lucro_real", "created_on", "updated_at", 
                           "created_by", "updated_by", "tenant_id"]

class ProjecaoCaixaSerializer(serializers.ModelSerializer):
    saldo_projetado_dia = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = ProjecaoCaixa
        fields = [
            "id", "data", "entradas_previstas", "saidas_previstas", 
            "saldo_projetado_dia", "created_on", "updated_at",
            "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = ["id", "saldo_projetado_dia", "created_on", "updated_at",
                           "created_by", "updated_by", "tenant_id"]

# --- Serializers for Report Generation (Read-only) ---

class FinancialSummarySerializer(serializers.Serializer):
    # Based on the previous OpenAPI definition
    month = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    receita_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    despesa_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    lucro_prejuizo = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    margem_lucro_percentual = serializers.FloatField(read_only=True)
    meta_lucro = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, allow_null=True)
    meta_atingida_percentual = serializers.FloatField(read_only=True, allow_null=True)
    contas_em_aberto_valor = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_estoque_valor = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class CashFlowEntrySerializer(serializers.Serializer):
    data = serializers.DateField(read_only=True)
    entrada = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    saida = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    saldo_diario = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class CashFlowReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    saldo_inicial = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    entries = CashFlowEntrySerializer(many=True, read_only=True)
    saldo_final = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class ExpenseByCategoryEntrySerializer(serializers.Serializer):
    categoria_id = serializers.IntegerField(read_only=True)
    categoria_nome = serializers.CharField(read_only=True)
    total_valor = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class ExpenseByCategoryReportSerializer(serializers.Serializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    entries = ExpenseByCategoryEntrySerializer(many=True, read_only=True)
