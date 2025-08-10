from django.conf import settings
from django.contrib.auth import authenticate
from django.core.files.storage import default_storage
from core.custom_fields.fields import FileOrUrlField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import User, Tenant, Domain, Address
from core.services.upload import save_upload_file, ALLOWED_IMAGE_EXTENSIONS
from rest_framework.exceptions import ValidationError
from django_tenants.utils import schema_context
import traceback

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
    # Campos do Tenant
    name = serializers.CharField()
    schema_name = serializers.CharField()
    document = serializers.CharField()
    logo = FileOrUrlField(required=False, allowed_types=["image/png", "image/jpeg"])
    # Campos do User (admin)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=False, allow_blank=True)
    avatar = FileOrUrlField(required=False, allowed_types=["image/png", "image/jpeg"])
    acceptance = serializers.BooleanField()
    # Campos do Address
    zipcode = serializers.CharField()
    address = serializers.CharField()
    address_number = serializers.CharField()
    complement = serializers.CharField(required=False, allow_blank=True)
    neighborhood = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    country = serializers.CharField()

    def validate(self, data):
        with schema_context("public"):
            errors = {}
            
            if Tenant.objects.filter(document=data['document']).exists():
                errors['document'] = ["Já existe uma empresa cadastrada com esse documento."]
            if User.objects.filter(email=data['email']).exists():
                errors['email'] = ["Este e-mail já está em uso."]
            if data.get("password") != data.get("repeat_password"):
                errors['repeat_password'] = ["As senhas não conferem."]
            if not data.get("acceptance"):
                errors['acceptance'] = ["Você deve aceitar os termos de uso."]
            if errors:
                raise ValidationError(errors)
        return data

    def create(self, validated_data):
        logo_url = None
        avatar_url = None
        logo_tmp_path = None
        avatar_tmp_path = None

        schema_name = validated_data['schema_name']
        logo_file = validated_data.get("logo")
        avatar_file = validated_data.get('avatar')

        with schema_context("public"):
            if hasattr(logo_file, "read"):
                try:
                    logo_url = save_upload_file(
                        logo_file,
                        domain=schema_name,
                        kind="logos",
                        is_image=True,
                        allowed_extensions=ALLOWED_IMAGE_EXTENSIONS,
                        max_size_mb=5
                    )
                    logo_tmp_path = logo_url.replace(settings.MEDIA_URL, "")
                except Exception as e:
                    if logo_tmp_path:
                        default_storage.delete(logo_tmp_path)
                    raise ValidationError({"logo": [f"Erro ao fazer upload do logo: {str(e)}"]})
            elif isinstance(logo_file, str):
                logo_url = validated_data.get("logo", "")

            
            if hasattr(avatar_file, "read"):
                try:
                    avatar_url = save_upload_file(
                        avatar_file,
                        domain=schema_name,
                        kind="avatars",
                        is_image=True,
                        allowed_extensions=ALLOWED_IMAGE_EXTENSIONS,
                        max_size_mb=5
                    )
                    avatar_tmp_path = avatar_url.replace(settings.MEDIA_URL, "")
                except Exception as e:
                    if avatar_tmp_path:
                        default_storage.delete(avatar_tmp_path)
                    raise ValidationError({"avatar": [f"Erro ao fazer upload do avatar: {str(e)}"]})
            elif isinstance(avatar_file, str):
                avatar_url = validated_data.get("avatar", "")

            try:
                with transaction.atomic():
                    print("Començando criação do tenant...")
                    tenant = Tenant.objects.create(
                        name=validated_data['name'],
                        schema_name=schema_name,
                        document=validated_data['document'],
                        logo=logo_url,
                    )

                    print("Tenant criado: ", tenant)
                    domain = Domain.objects.create(
                        domain=f"{schema_name}.{settings.PARENT_DOMAIN}",
                        tenant=tenant,
                        is_primary=True
                    )

                    print("Domínio criado: ", domain)
                    user = User.objects.create_user(
                        tenant=tenant,
                        email=validated_data['email'],
                        password=validated_data['password'],
                        nickname=validated_data.get('nickname', ''),
                        avatar=avatar_url,
                        acceptance=validated_data['acceptance'],
                        is_active=True,
                    )

                    print("Usuário admin criado: ", user)
                    address = Address.objects.create(
                        tenant=tenant,
                        zipcode=validated_data['zipcode'],
                        address=validated_data['address'],
                        address_number=validated_data['address_number'],
                        complement=validated_data.get('complement', ''),
                        neighborhood=validated_data['neighborhood'],
                        city=validated_data['city'],
                        state=validated_data['state'],
                        country=validated_data['country'],
                        created_by=user,
                        updated_by=user,
                    )

                    print("Endereço criado: ", address)
                    return tenant
            except Exception as e:
                print("Erro ao criar registro: ", str(e))
                traceback.print_exc()
                
                if logo_tmp_path:
                    default_storage.delete(logo_tmp_path)
                if avatar_tmp_path:
                    default_storage.delete(avatar_tmp_path)
                raise ValidationError({"non_field_errors": [f"Falha no cadastro: {str(e)}"]})
            
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(_('E-mail e senha são obrigatórios.'))

        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError(_("Request não disponível no context do serializer."))
            
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            raise serializers.ValidationError(_('Tenant não identificado.'))

        try:
            user = User.objects.get(email=email, tenant=tenant)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Usuário ou senha inválidos.'))

        user = authenticate(request=request, email=email, password=password)
        if not user:
            raise serializers.ValidationError(_('Usuário ou senha inválidos.'))

        if not user.is_active:
            raise serializers.ValidationError(_('Conta desativada.'))

        attrs['user'] = user
        attrs['tenant'] = tenant
        return attrs

