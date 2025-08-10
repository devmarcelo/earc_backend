# setup/urls_public.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from core.views import RegisterTenantView

from django.http import JsonResponse

def ping_public(_):
    return JsonResponse({"public": True, "ok": True})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/ping/", ping_public, name="public-ping"),
    path("register-company/", RegisterTenantView.as_view(), name="register-company"),
    # Auth endpoints (Login, Register, Refresh, OAuth) - Reside in public schema
    path("v1/auth/", include("core.urls_auth")), # Create this file later
    # API Schema (Swagger/Redoc) - Publicly accessible
    path("v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("v1/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Include other public-specific endpoints if any
]