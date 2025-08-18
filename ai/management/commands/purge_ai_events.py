from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Purge registros em ai.event por status e idade (minutos). Ex.: --status done --older-min 0"

    def add_arguments(self, parser):
        parser.add_argument("--status", action="append", required=True,
                            choices=["pending","processing","done","error"])
        parser.add_argument("--older-min", type=int, default=0)
        parser.add_argument("--batch", type=int, default=5000)

    def handle(self, *args, **opts):
        statuses = opts["status"]
        older_min = opts["older_min"]
        batch = opts["batch"]

        placeholders = ",".join(["%s"] * len(statuses))
        params_age = []
        age_sql = "TRUE"
        if older_min > 0:
            age_sql = "created_at < (now() - (%s || ' minutes')::interval)"
            params_age = [str(older_min)]

        total = 0
        with connection.cursor() as cur:
            while True:
                cur.execute(f"""
                  WITH del AS (
                    SELECT id FROM ai.event
                     WHERE status IN ({placeholders})
                       AND {age_sql}
                     ORDER BY id
                     LIMIT %s
                  )
                  DELETE FROM ai.event e
                   USING del
                   WHERE e.id = del.id
                  RETURNING e.id
                """, [*statuses, *params_age, batch])
                n = len(cur.fetchall())
                total += n
                if n < batch:
                    break

        self.stdout.write(self.style.SUCCESS(f"Purged: {total}"))
