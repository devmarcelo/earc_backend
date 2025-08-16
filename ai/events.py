import json
from django.db import connection

def emit_event(action: str, payload: dict, tenant_schema: str, source: str = "api"):
    with connection.cursor() as cur:
        cur.execute(
            "INSERT INTO ai.event (tenant_schema, action, source, payload) VALUES (%s, %s, %s, %s::jsonb)",
            [tenant_schema, action, source, json.dumps(payload or {})],
        )
