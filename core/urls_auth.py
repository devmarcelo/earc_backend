# core/urls_auth.py
from core.views import LoginView
from django.urls import path, include
from core.views import TokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
)
# Import your custom registration view if you create one
# from .views import RegisterTenantView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    # JWT Authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Custom Tenant Registration Endpoint (Example - needs view implementation)
    # path("register-tenant/", RegisterTenantView.as_view(), name="register_tenant"),
    path("password/", include("core.reset_password.urls")),
]

