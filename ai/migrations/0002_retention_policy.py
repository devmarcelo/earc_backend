from django.db import migrations

UP = r"""
-- índices parciais para limpeza rápida
CREATE INDEX IF NOT EXISTS ix_ai_event_done_old
  ON ai.event (created_at) WHERE status = 'done';

CREATE INDEX IF NOT EXISTS ix_ai_event_error_old
  ON ai.event (created_at) WHERE status = 'error';

CREATE INDEX IF NOT EXISTS ix_ai_rec_status_old
  ON ai.recommendation (created_at)
  WHERE status IN ('ack','dismissed','applied','expired');
"""

DOWN = r"""
DROP INDEX IF EXISTS ix_ai_event_done_old;
DROP INDEX IF EXISTS ix_ai_event_error_old;
DROP INDEX IF EXISTS ix_ai_rec_status_old;
"""

class Migration(migrations.Migration):
    dependencies = [("ai", "0001_ai_schema")]
    operations = [migrations.RunSQL(UP, DOWN)]
