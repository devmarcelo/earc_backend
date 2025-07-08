from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Tenant, Domain, User, Address

# Somente superuser pode editar/criar/deletar User e Address
class SuperuserEditMixin:
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

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

@admin.register(User)
class UserAdmin(SuperuserEditMixin, BaseUserAdmin):
    list_display = ("email", "nickname", "phone", "is_active", "is_staff", "tenant", "last_login", "created_on")
    search_fields = ("email", "nickname", "phone")
    list_filter = ("is_active", "is_staff", "tenant")
    readonly_fields = ("last_login", "created_on", "updated_on", "tenant", "is_anonymized")
    ordering = ("-created_on",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("nickname", "phone", "avatar", "acceptance")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_on", "updated_on")}),
    )

@admin.register(Address)
class AddressAdmin(SuperuserEditMixin, admin.ModelAdmin):
    list_display = ("address", "address_number", "city", "state", "zipcode", "tenant", "is_active", "created_on")
    search_fields = ("address", "city", "state", "zipcode")
    list_filter = ("is_active", "city", "state", "tenant")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")
    ordering = ("-created_on",)
    actions = None
