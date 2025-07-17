# core/logging.py
import logging
from django.db import connection

class TenantLogFilter(logging.Filter):
    def filter(self, record):
        try:
            tenant = getattr(connection, 'tenant', None)
            record.tenant = getattr(tenant, 'schema_name', 'public') if tenant else 'public'
        except Exception:
            record.tenant = 'unknown'
        return True
