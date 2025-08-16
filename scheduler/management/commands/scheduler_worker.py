# core_scheduler/management/commands/scheduler_worker.py
import importlib, time, logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import models  # <-- necessário para models.Q
from django.utils import timezone
from django_tenants.utils import schema_context
from scheduler.models import Job, SchedulerControl

log = logging.getLogger("core.ai")

def _acquire_job():
    now = timezone.now()
    with transaction.atomic():
        job = (Job.objects
               .select_for_update(skip_locked=True)
               .filter(enabled=True)
               .filter(models.Q(next_run_at__lte=now) | models.Q(next_run_at__isnull=True))
               .filter(models.Q(lock_until__lte=now) | models.Q(lock_until__isnull=True))
               .order_by("next_run_at", "id")
               .first())
        if not job:
            return None
        job.lock_until = now + timezone.timedelta(seconds=job.max_runtime_seconds)
        job.save(update_fields=["lock_until"])
        return job

def _run_handler(job: Job):
    module_name, func_name = job.handler.rsplit(":", 1)
    func = getattr(importlib.import_module(module_name), func_name)
    if job.tenant_schema:
        with schema_context(job.tenant_schema):
            func(**(job.args or {}))
    else:
        func(**(job.args or {}))

class Command(BaseCommand):
    help = "Lightweight DB-backed scheduler (no Celery)."

    def add_arguments(self, parser):
        parser.add_argument("--loop", action="store_true")
        parser.add_argument("--sleep", type=float, default=1.0)

    def handle(self, *args, **opts):
        loop = opts["loop"]; sleep_s = opts["sleep"]
        self.stdout.write(self.style.SUCCESS("Scheduler up."))
        while True:
            if SchedulerControl.paused():
                time.sleep(sleep_s); 
                if not loop: break
                continue
            job = _acquire_job()
            if not job:
                time.sleep(sleep_s)
                if not loop: break
                continue
            try:
                _run_handler(job)
                job.consecutive_failures = 0
            except Exception as e:
                log.exception("Job %s failed: %s", job.name, e)
                job.consecutive_failures += 1
            finally:
                job.lock_until = None
                job.schedule_next()
            if not loop:
                break
