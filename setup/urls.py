# setup/urls.py (Tenant-specific URLs)
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.social.views import GoogleLoginView

urlpatterns = [
    # OpenAPI JSON
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI (interativa)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc (opcional)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Include API endpoit for social account
    path("api/v1/auth/social/google/", GoogleLoginView.as_view(), name="google-login"),
    
    # Include API endpoints for tenant-specific apps
    path("api/", include("setup.urls_public")),
    path("api/v1/financial/", include("financial.urls")), # Create later
    path("api/v1/inventory/", include("inventory.urls")), # Create later
    path("api/v1/hr/", include("hr.urls")),             # Create later
    path("api/v1/reports/", include("reports.urls")),     # Create later
    path("api/v1/settings/", include("settings_app.urls")), # Create later

    # Include other tenant-specific URL patterns here
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

