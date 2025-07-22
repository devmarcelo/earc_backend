from core.models import Tenant
from rest_framework import serializers
from django.conf import settings

class PublicTenantSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    theme = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = [
            "name",
            "schema_name",
            "logo",
            "theme",
            "is_active",
        ]

    def get_logo(self, obj):
        request = self.context.get("request")
        
        if obj.logo:
            if request:
                return request.build_absolute_uri(obj.logo)
            else:
                return settings.BASE_URL + obj.logo

        return None

    def get_theme(self, obj):
        # Adapte para retornar apenas chaves públicas seguras
        theme = obj.theme_settings or {}
        return {
            "primary_color": theme.get("primary_color", "#F96C20"),
            "background": theme.get("background", "#FFF7F0"),
            "custom_login_message": theme.get("custom_login_message", f"Bem-vindo à {obj.name}!")
        }

