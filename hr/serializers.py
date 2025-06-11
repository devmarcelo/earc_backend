# hr/serializers.py
from rest_framework import serializers
from .models import Funcionario

class FuncionarioSerializer(serializers.ModelSerializer):
    custo_total_aproximado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Funcionario
        fields = [
            "id", "nome", "cargo", "salario_base", "encargos_percentual", 
            "data_proximo_pagamento", "custo_total_aproximado",
            "created_on", "updated_at", "created_by", "updated_by"
        ]
        read_only_fields = ["id", "custo_total_aproximado", "created_on", "updated_at", "created_by", "updated_by"]
