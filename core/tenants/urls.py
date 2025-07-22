from django.urls import path
from .views import PublicTenantSettingsView

urlpatterns = [
    path("<slug:slug>/public-settings/", PublicTenantSettingsView.as_view(), name="tenant-public-settings",),
]
