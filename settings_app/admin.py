from django.contrib import admin
from .models import Parameter, Integration

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "tenant", "is_active", "created_on")
    search_fields = ("key", "value", "description")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "tenant", "is_active", "created_on")
    search_fields = ("name", "service", "description")
    list_filter = ("tenant", "service", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")
