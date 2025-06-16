# financial/serializers.py
from rest_framework import serializers
from .models import Cliente, Fornecedor, Receita, Despesa, ContaPagarReceber
from core.serializers import CategoriaSerializer # Reuse Categoria serializer
from core.models import Categoria, User

# --- Cliente Serializers ---
class ClienteSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    class Meta:
        model = Cliente
        fields = ["id", "nome", "contato", "endereco", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]
        read_only_fields = ["id", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

# --- Fornecedor Serializers ---
class FornecedorSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = ["id", "nome", "contato", "cnpj", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]
        read_only_fields = ["id", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

# --- Receita Serializers ---
class ReceitaSerializer(serializers.ModelSerializer):
    # Use nested serializers for related fields for read operations
    cliente = ClienteSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    # Use PrimaryKeyRelatedField for write operations
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source="cliente", write_only=True, required=False, allow_null=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.filter(tipo="Receita"), source="categoria", write_only=True
    )

    class Meta:
        model = Receita
        fields = [
            "id", "data", "descricao", "valor", 
            "cliente", "categoria", # Read-only nested
            "cliente_id", "categoria_id", # Write-only PKs
            "created_on", "updated_at", "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = ["id", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

    def validate_categoria_id(self, value):
        """Ensure the category is of type Receita."""
        if value.tipo != "Receita":
            raise serializers.ValidationError("A categoria selecionada não é do tipo Receita.")
        return value

# --- Despesa Serializers ---
class DespesaSerializer(serializers.ModelSerializer):
    fornecedor = FornecedorSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    fornecedor_id = serializers.PrimaryKeyRelatedField(
        queryset=Fornecedor.objects.all(), source="fornecedor", write_only=True, required=False, allow_null=True
    )
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.filter(tipo="Despesa"), source="categoria", write_only=True
    )

    class Meta:
        model = Despesa
        fields = [
            "id", "data", "descricao", "valor", 
            "fornecedor", "categoria", # Read-only nested
            "fornecedor_id", "categoria_id", # Write-only PKs
            "created_on", "updated_at", "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = ["id", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

    def validate_categoria_id(self, value):
        """Ensure the category is of type Despesa."""
        if value.tipo != "Despesa":
            raise serializers.ValidationError("A categoria selecionada não é do tipo Despesa.")
        return value

# --- ContaPagarReceber Serializers ---
class ContaPagarReceberSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    fornecedor = FornecedorSerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), source="cliente", write_only=True, required=False, allow_null=True
    )
    fornecedor_id = serializers.PrimaryKeyRelatedField(
        queryset=Fornecedor.objects.all(), source="fornecedor", write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ContaPagarReceber
        fields = [
            "id", "tipo", "descricao", "valor", "data_vencimento", "status", "data_pagamento",
            "cliente", "fornecedor", # Read-only nested
            "cliente_id", "fornecedor_id", # Write-only PKs
            "created_on", "updated_at", "created_by", "updated_by", "tenant_id"
        ]
        # Status might be read-only depending on how updates are handled (e.g., separate endpoint to mark as paid)
        read_only_fields = ["id", "status", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

    def validate(self, data):
        """Ensure either cliente_id or fornecedor_id is provided based on tipo."""
        tipo = data.get("tipo")
        cliente_id = data.get("cliente") # Get the object if nested, or the ID if write_only
        fornecedor_id = data.get("fornecedor") # Get the object if nested, or the ID if write_only

        # During write operations, client_id/fornecedor_id are the actual fields being submitted
        # Check the source fields directly
        submitted_cliente = data.get("cliente")
        submitted_fornecedor = data.get("fornecedor")

        if tipo == "Receber" and not submitted_cliente:
            raise serializers.ValidationError({"cliente_id": "Cliente é obrigatório para contas a receber."}) 
        if tipo == "Pagar" and not submitted_fornecedor:
             raise serializers.ValidationError({"fornecedor_id": "Fornecedor é obrigatório para contas a pagar."}) 
        if tipo == "Receber" and submitted_fornecedor:
            raise serializers.ValidationError({"fornecedor_id": "Fornecedor não deve ser informado para contas a receber."}) 
        if tipo == "Pagar" and submitted_cliente:
            raise serializers.ValidationError({"cliente_id": "Cliente não deve ser informado para contas a pagar."}) 
        return data

# Serializer for marking an account as paid (PATCH request)
class MarkAsPaidSerializer(serializers.Serializer):
    data_pagamento = serializers.DateField(required=True)

    def update(self, instance, validated_data):
        instance.status = "Pago"
        instance.data_pagamento = validated_data["data_pagamento"]
        # Ensure updated_by is set from the request context
        if 'request' in self.context and hasattr(self.context['request'], 'user'):
            instance.updated_by = self.context['request'].user
        instance.save(update_fields=["status", "data_pagamento", "updated_at", "updated_by"])
        return instance
