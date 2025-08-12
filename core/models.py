from django.db import models
from django.conf import settings
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    name = models.CharField(max_length=100, unique=True)  # schema_name
    document = models.CharField(max_length=50, unique=True)  # CNPJ/CPF/ID legal
    logo = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_anonymized = models.BooleanField(default=False)
    theme_settings = models.JSONField(default=dict, blank=True, null=True)
    auto_create_schema = True

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['document']),
        ]
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def anonymize(self):
        self.name = ""
        self.document = ""
        self.logo = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

class TenantAwareModel(models.Model):
    tenant = models.ForeignKey('core.Tenant', on_delete=models.CASCADE, null=True, blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_updated")
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

