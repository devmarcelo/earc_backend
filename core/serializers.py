# core/serializers.py
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
    # Domain name will be derived or set separately, e.g., company_name.localhost
    # domain_name = serializers.CharField(max_length=253)
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True, min_length=8)

    def create(self, validated_data):
        tenant = Tenant.objects.create(
            name=validated_data["company_name"],
            schema_name=validated_data["company_name"].lower().replace(" ", "") # Simple schema name generation
        )
        # Create domain (adjust logic as needed, e.g., using environment variable for base domain)
        domain = Domain.objects.create(
            domain=f"{tenant.schema_name}.localhost", # Example for local dev
            tenant=tenant,
            is_primary=True
        )

        # Create the admin user within the new tenant's schema
        with schema_context(tenant.schema_name):
            admin_user = UserModel.objects.create_user(
                email=validated_data["admin_email"],
                password=validated_data["admin_password"],
                tenant=tenant, # Associate user with the tenant
                is_staff=True, # Optional: Allow access to admin if enabled
                is_superuser=True # Optional: Grant superuser within tenant schema
            )
            # You might want to assign specific roles/permissions here

        return {
            "tenant": tenant,
            "domain": domain,
            "admin_user": admin_user
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
