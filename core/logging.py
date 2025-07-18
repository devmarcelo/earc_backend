# core/logg.py
import logging
import os
from django.db import connection

class TenantLogFilter(logging.Filter):
    """
    Logging filter que insere o schema do tenant atual em cada registro de log.
    - Usa connection.tenant para obter o schema_name.
    - Fallback para 'public' se não houver tenant (admin, comandos).
    - Fallback para 'unknown' em caso de exceções.
    - Opcional: adiciona nome do ambiente no record (ex: dev, prod).
    """
    def filter(self, record):
        try:
            tenant = getattr(connection, 'tenant', None)
            record.tenant = getattr(tenant, 'schema_name', 'public') if tenant else 'public'
        except Exception:
            record.tenant = 'unknown'
        # Opcional: ambiente no log (facilita buscas em log aggregator)
        record.env = os.environ.get("ENVIRONMENT", "development")
        return True
