# core/serializers.py
import os
from rest_framework import serializers
from .models import User, Tenant, Domain, Categoria # Import Categoria here
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context

UserModel = get_user_model()

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "name", "created_on", "updated_at", "theme_settings"]
        read_only_fields = ["id", "created_on", "updated_at"]

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "domain", "is_primary", "tenant"]
        read_only_fields = ["id", "tenant"]

class UserSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "email", "first_name", "last_name", "tenant", "is_active", "date_joined"]
        read_only_fields = ["id", "tenant", "is_active", "date_joined"]

class RegisterTenantSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=100)
    schema_name = serializers.SlugField(max_length=50)
    # Domain name will be derived or set separately, e.g., company_name.localhost
    # domain_name = serializers.CharField(max_length=253)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    apelido = serializers.CharField(max_length=100, required=False, allow_blank=True)
    imagem = serializers.URLField(required=False, allow_blank=True)

    def create(self, validated_data):
        company_name = validated_data["company_name"]
        schema_name = validated_data["schema_name"].lower().replace(" ", "")

        email = validated_data["email"]
        password = validated_data["password"]
        apelido = validated_data.get("apelido", "")
        imagem = validated_data.get("imagem", "")

        # 1. Criação do Tenant
        tenant = Tenant.objects.create(
            name=company_name,
            schema_name=schema_name
        )
        
        # 2. Criação do Domain dinâmico
        base_domain = os.environ.get("DB_HOST", "localhost")
        domain = Domain.objects.create(
            domain=f"{schema_name}.{base_domain}",
            tenant=tenant,
            is_primary=True
        )

        # 3. Migração de schema para o novo tenant
        from django.core.management import call_command
        call_command("migrate_schemas", schema_name=schema_name, interactive=False)

        # 4. Criação do usuário admin no contexto do novo tenant
        with schema_context(schema_name):
            user = User.objects.create_user(
                email=email,
                password=password,
                apelido=apelido,
                imagem=imagem,
                is_staff=True,
                is_superuser=True,
                tenant=tenant
            )

        return {
            "tenant": tenant,
            "domain": domain,
            "user": user
        }

# Serializer for Categoria (often needed across apps)
class CategoriaSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)
    
    class Meta:
        model = Categoria
        fields = ["id", "nome", "tipo", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]
        read_only_fields = ["id", "created_on", "updated_at", "created_by", "updated_by", "tenant_id"]

    # Add validation if needed, e.g., ensure unique name per type within tenant context
    # def validate(self, data):
    #     # Access tenant from context if passed in view
    #     tenant = self.context["request"].tenant
    #     nome = data.get("nome")
    #     tipo = data.get("tipo")
    #     instance_id = self.instance.id if self.instance else None
    #     query = Categoria.objects.filter(tenant=tenant, nome=nome, tipo=tipo)
    #     if instance_id:
    #         query = query.exclude(pk=instance_id)
    #     if query.exists():
    #         raise serializers.ValidationError(f"Categoria ", {nome}, " do tipo ", {tipo}, " já existe.")
    #     return data
