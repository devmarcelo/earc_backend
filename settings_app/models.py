# settings_app/models.py
from django.db import models

# No specific models needed here for now.
# Tenant-specific settings like theme are stored in core.Tenant model (theme_settings JSONField).
# User management is handled via core.User.

# If specific, granular settings per tenant are needed later,
# they can be added here as a TenantAwareModel.
# Example:
# from core.models import TenantAwareModel
# class TenantConfiguration(TenantAwareModel):
#     enable_feature_x = models.BooleanField(default=False)
#     notification_preference = models.CharField(max_length=50, default=\"email\")
#     # ... other settings

