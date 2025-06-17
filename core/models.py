# core/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O campo email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme_settings = models.JSONField(default=dict, blank=True, null=True)
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email address")
    apelido = models.CharField(max_length=100, null=True, blank=True)
    imagem = models.URLField(null=True, blank=True)  # Pode armazenar URL externa (Google) ou do sistema
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.apelido or self.email

# --- Tenant-Specific Models (Managed within Tenant Schemas) ---

# Base model for tenant-specific tables (optional, but good for common fields)
class TenantAwareModel(models.Model):
    # Explicit tenant field for audit purposes (even though django-tenants handles schema isolation)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    # tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE) # Handled implicitly by django-tenants for models in TENANT_APPS
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updated")

    class Meta:
        abstract = True

class Categoria(TenantAwareModel):
    TIPO_CHOICES = [
        ("Receita", "Receita"),
        ("Despesa", "Despesa"),
        ("Estoque", "Estoque"),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    # tenant field is implicit via django-tenants

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        # Ensure unique category name per type within a tenant
        # Note: django-tenants doesn't automatically add tenant_id to unique_together
        # This needs careful handling during migrations or potentially a custom constraint.
        # unique_together = (
        #     ("tenant", "nome", "tipo"), # Requires tenant field to be explicit if used here
        # )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
