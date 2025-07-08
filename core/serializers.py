from rest_framework import serializers
from .models import User, Tenant, Domain, Address

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'document',
            'logo',
            'created_on',
            'updated_on',
            'is_active',
            'is_anonymized',
            'theme_settings'
        ]
        read_only_fields = ('created_on', 'updated_on', 'is_anonymized')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'tenant',
            'zipcode',
            'address',
            'address_number',
            'complement',
            'neighborhood',
            'city',
            'state',
            'country',
            'created_on',
            'updated_on',
            'is_active',
            'is_anonymized',
        ]
        read_only_fields = ('created_on', 'updated_on', 'is_anonymized')

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = [
            'id',
            'domain',
            'tenant',
            'is_primary'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone',
            'nickname',
            'avatar',
            'acceptance',
            'is_active',
            'is_anonymized',
            'tenant',
            'created_on',
            'updated_on',
        ]
        read_only_fields = ('created_on', 'updated_on', 'is_anonymized')

class RegisterTenantSerializer(serializers.Serializer):
    # Para cadastro simultâneo de Tenant, User (admin) e Address
    company_name = serializers.CharField(max_length=100)
    schema_name = serializers.CharField(max_length=100)
    document = serializers.CharField(max_length=50)
    logo = serializers.URLField(allow_blank=True, required=False)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100, allow_blank=True, required=False)
    avatar = serializers.URLField(allow_blank=True, required=False)
    acceptance = serializers.BooleanField()
    zipcode = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=200)
    address_number = serializers.CharField(max_length=20)
    complement = serializers.CharField(max_length=100, allow_blank=True, required=False)
    neighborhood = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)

    def validate(self, data):
        if data.get('password') != data.get('repeat_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    # Implementação de create() ficaria no view, utilizando Tenant, User, Address

