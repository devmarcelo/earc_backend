# setup/urls.py (Tenant-specific URLs)
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Include API endpoints for tenant-specific apps
    path("api/v1/financial/", include("financial.urls")), # Create later
    path("api/v1/inventory/", include("inventory.urls")), # Create later
    path("api/v1/hr/", include("hr.urls")),             # Create later
    path("api/v1/reports/", include("reports.urls")),     # Create later
    path("api/v1/settings/", include("settings_app.urls")), # Create later
    path("api/v1/categories/", include("core.urls_categories")), # Categories might be shared or managed centrally, place appropriately

    # Include other tenant-specific URL patterns here
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

