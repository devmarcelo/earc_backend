from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address

# Somente superuser pode editar/criar/deletar User e Address
class SuperuserEditMixin:
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(User)
class UserAdmin(SuperuserEditMixin, BaseUserAdmin):
    model = User
    list_display = ("id", "email", "nickname", "is_active", "is_staff", "is_superuser")
    ordering = ("email",)
    list_filter = ("is_active", "is_staff", "tenant")
    readonly_fields = ("last_login", "created_on", "updated_on", "tenant", "is_anonymized")
    search_fields = ("email", "nickname", "phone")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("nickname", "phone", "avatar", "acceptance")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_on", "updated_on")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

@admin.register(Address)
class AddressAdmin(SuperuserEditMixin, admin.ModelAdmin):
    list_display = ("id", "city", "state", "tenant", "is_active")
    search_fields = ("city", "state", "address", "zipcode")
    list_filter = ("is_active", "city", "state", "tenant")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")
    ordering = ("-created_on",)
    actions = None
