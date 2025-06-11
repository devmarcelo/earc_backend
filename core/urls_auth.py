# core/urls_auth.py
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
# Import your custom registration view if you create one
# from .views import RegisterTenantView

urlpatterns = [
    # JWT Authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Django-allauth URLs for account management (password reset, email confirmation, etc.)
    # These typically render templates, adjust if using DRF adapters for allauth
    path("", include("allauth.urls")), 

    # Custom Tenant Registration Endpoint (Example - needs view implementation)
    # path("register-tenant/", RegisterTenantView.as_view(), name="register_tenant"),
]

