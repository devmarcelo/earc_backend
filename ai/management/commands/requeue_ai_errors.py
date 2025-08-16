from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Reagenda eventos com status=error para pending."

    def handle(self, *args, **opts):
        with connection.cursor() as cur:
            cur.execute("UPDATE ai.event SET status='pending', error=NULL WHERE status='error'")
            n = cur.rowcount
        self.stdout.write(self.style.SUCCESS(f"Requeued: {n}"))
