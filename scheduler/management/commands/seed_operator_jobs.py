from django.core.management.base import BaseCommand
from scheduler.models import Job

def upsert_job(name, handler, args=None, interval_seconds=3600, enabled=True):
    job, created = Job.objects.get_or_create(name=name, defaults={
        "handler": handler,
        "args": args or {},
        "interval_seconds": interval_seconds,
        "enabled": enabled,
        "tenant_schema": None,
    })

    if not created:
        job.handler = handler
        job.args = args or {}
        job.interval_seconds = interval_seconds
        job.enabled = enabled
        job.save()
    return job

class Command(BaseCommand):
    help = "Seed operator jobs (AI processing + cleanup)."

    def handle(self, *args, **opts):
        upsert_job("AI: Process events", "ai.jobs:process_ai_events", {"batch_size": 200}, interval_seconds=5)
        upsert_job("AI: Cleanup events", "ai.jobs:cleanup_events", {"batch_size": 2000}, interval_seconds=600)           # 10 min
        upsert_job("AI: Cleanup recommendations", "ai.jobs:cleanup_recommendations", {"batch_size": 2000}, interval_seconds=600)  # 10 min
        self.stdout.write(self.style.SUCCESS("OK: operator jobs seeded/updated"))
