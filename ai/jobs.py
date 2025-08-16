# ai/jobs.py
import json, os
from django.db import connection
from django.utils import timezone
from ai.skills import cash_autopilot, engagement

ROUTES = [
    ("finance.",  cash_autopilot.recommendations_for_event),
    ("auth.",     engagement.recommendations_for_event),
]

def _dispatch(action: str, payload: dict):
    for prefix, handler in ROUTES:
        if action.startswith(prefix):
            return handler(action, payload) or []
    return []

def _to_dict(p):
    if p is None: return {}
    if isinstance(p, dict): return p
    if isinstance(p, (bytes, bytearray)): p = p.decode("utf-8","ignore")
    if isinstance(p, str):
        try: return json.loads(p) if p else {}
        except Exception: return {}
    return {}

def process_ai_events(batch_size: int = 200) -> int:
    processed = 0
    with connection.cursor() as cur:
        cur.execute("""
        WITH next AS (
          SELECT id FROM ai.event
           WHERE status = 'pending'
           ORDER BY created_at
           FOR UPDATE SKIP LOCKED
           LIMIT %s
        )
        UPDATE ai.event e
           SET status = 'processing'
          FROM next
         WHERE e.id = next.id
        RETURNING e.id, e.tenant_schema, e.action, e.payload::text
        """, [batch_size])
        rows = cur.fetchall()

        for ev_id, tenant_schema, action, payload_raw in rows:
            try:
                payload = _to_dict(payload_raw)
                recs = _dispatch(action, payload)
                for rec in recs:
                    cur.execute(
                        "INSERT INTO ai.recommendation (tenant_schema, kind, title, details) VALUES (%s,%s,%s,%s::jsonb)",
                        [tenant_schema, rec.get("kind","info"), rec.get("title","Recommendation"), json.dumps(rec.get("details",{}))]
                    )

                cur.execute("DELETE FROM ai.event WHERE id=%s", [ev_id])
                processed += 1
            except Exception as exc:
                cur.execute("UPDATE ai.event SET status='error', error=%s WHERE id=%s", [str(exc), ev_id])
    return processed

def cleanup_events(batch_size: int = 2000) -> int:
    """ processing travado -> pending; error > 24h -> delete """
    n_total = 0
    with connection.cursor() as cur:
        # destravar 'processing' com mais de 5min
        cur.execute("""
          UPDATE ai.event
             SET status='pending', error=NULL
           WHERE status='processing'
             AND created_at < (now() - interval '5 minutes')
        """)
        # delete errors com mais de 24h em lotes
        while True:
            cur.execute("""
              WITH del AS (
                SELECT id FROM ai.event
                 WHERE status='error'
                   AND created_at < (now() - interval '24 hours')
                 ORDER BY created_at
                 LIMIT %s
              )
              DELETE FROM ai.event e
               USING del
               WHERE e.id=del.id
              RETURNING e.id
            """, [batch_size])
            deleted = cur.fetchall()
            n_total += len(deleted)
            if len(deleted) < batch_size:
                break
    return n_total

def cleanup_recommendations(batch_size: int = 2000) -> int:
    """ new > 24h -> delete (ninguém usou) """
    n_total = 0
    with connection.cursor() as cur:
        while True:
            cur.execute("""
              WITH del AS (
                SELECT id FROM ai.recommendation
                 WHERE status='new'
                   AND created_at < (now() - interval '24 hours')
                 ORDER BY created_at
                 LIMIT %s
              )
              DELETE FROM ai.recommendation r
               USING del
               WHERE r.id=del.id
              RETURNING r.id
            """, [batch_size])
            deleted = cur.fetchall()
            n_total += len(deleted)
            if len(deleted) < batch_size:
                break
    return n_total
