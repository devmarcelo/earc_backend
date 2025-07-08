from django.db import models
from core.models import TenantAwareModel

class Parameter(TenantAwareModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'key']),
        ]
        verbose_name = 'Parameter'
        verbose_name_plural = 'Parameters'

    def anonymize(self):
        self.value = ""
        self.description = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.key

class Integration(TenantAwareModel):
    name = models.CharField(max_length=150)
    service = models.CharField(max_length=100)
    credentials = models.JSONField(default=dict, blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'service']),
        ]
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'

    def anonymize(self):
        self.name = ""
        self.credentials = {}
        self.description = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name
