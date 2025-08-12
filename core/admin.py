from django.contrib import admin
from .models import Tenant, Domain

# Tenant e Domain apenas leitura (não pode editar/criar/deletar pelo admin)
class NoDeleteMixin:
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Tenant)
class TenantAdmin(NoDeleteMixin, admin.ModelAdmin):
    list_display = ("name", "document", "is_active", "created_on", "updated_on")
    search_fields = ("name", "document")
    list_filter = ("is_active",)
    readonly_fields = ("name", "document", "created_on", "updated_on", "theme_settings", "auto_create_schema", "is_anonymized")
    ordering = ("-created_on",)
    actions = None

@admin.register(Domain)
class DomainAdmin(NoDeleteMixin, admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")
    search_fields = ("domain",)
    readonly_fields = ("domain", "tenant", "is_primary")
    ordering = ("tenant",)
    actions = None
