# inventory/serializers.py
from rest_framework import serializers
from .models import ItemEstoque
from core.serializers import CategoriaSerializer # Reuse Categoria serializer
from core.models import Categoria

class ItemEstoqueSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.filter(tipo="Estoque"), source="categoria", write_only=True
    )
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ItemEstoque
        fields = [
            "id", "nome_produto", "quantidade", "custo_unitario", "valor_total",
            "categoria", # Read-only nested
            "categoria_id", # Write-only PK
            "created_on", "updated_at", "created_by", "updated_by"
        ]
        read_only_fields = ["id", "valor_total", "created_on", "updated_at", "created_by", "updated_by"]

    def validate_categoria_id(self, value):
        """Ensure the category is of type Estoque."""
        if value.tipo != "Estoque":
            raise serializers.ValidationError("A categoria selecionada não é do tipo Estoque.")
        return value
