from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    User por-tenant (não existe no schema público).
    Login por e-mail, sem username.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="email address")
    phone = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    acceptance = models.BooleanField(default=False)
    is_anonymized = models.BooleanField(default=False)

    # FK para o Tenant (definido no core) – mantemos para coerência com seu modelo
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'email']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def anonymize(self):
        self.email = ""
        self.phone = ""
        self.nickname = ""
        self.avatar = ""
        self.acceptance = False
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.nickname or self.email

class Address(models.Model):
    """
    Address por-tenant. Herdava um TenantAwareModel em core — vamos ficar
    independentes aqui para não travar a refatoração de imediato.
    """
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="address_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="address_updated")
    is_active = models.BooleanField(default=True)

    zipcode = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    address_number = models.CharField(max_length=20)
    complement = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'city']),
        ]
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def anonymize(self):
        self.zipcode = ""
        self.address = ""
        self.address_number = ""
        self.complement = ""
        self.neighborhood = ""
        self.city = ""
        self.state = ""
        self.country = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return f"{self.address}, {self.address_number} - {self.city}/{self.state}"
