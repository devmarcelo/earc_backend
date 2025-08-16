from django.db import migrations

UP = r"""
CREATE SCHEMA IF NOT EXISTS ai;

CREATE TABLE IF NOT EXISTS ai.event (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  tenant_schema TEXT NOT NULL,
  action TEXT NOT NULL,
  source TEXT,
  payload JSONB NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'pending', -- pending|processing|done|error
  error TEXT
);

CREATE INDEX IF NOT EXISTS ix_ai_event_tenant ON ai.event(tenant_schema, created_at);
CREATE INDEX IF NOT EXISTS ix_ai_event_action ON ai.event(action, created_at);

CREATE TABLE IF NOT EXISTS ai.recommendation (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  tenant_schema TEXT NOT NULL,
  kind TEXT NOT NULL,           -- ex.: 'cash', 'stock', 'engagement'
  title TEXT NOT NULL,
  details JSONB NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'new' -- new|ack|dismissed|applied
);
CREATE INDEX IF NOT EXISTS ix_ai_rec_tenant ON ai.recommendation(tenant_schema, created_at);
"""

DOWN = r"""
DROP TABLE IF EXISTS ai.recommendation;
DROP TABLE IF EXISTS ai.event;
"""

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.RunSQL(UP, DOWN)]
