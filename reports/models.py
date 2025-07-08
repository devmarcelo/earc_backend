from django.db import models
from core.models import TenantAwareModel

class Report(TenantAwareModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    report_type = models.CharField(max_length=50)
    parameters = models.JSONField(default=dict, blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'report_type']),
            models.Index(fields=['tenant', 'generated_at']),
        ]
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def anonymize(self):
        self.name = ""
        self.description = ""
        self.parameters = {}
        self.file_url = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name
