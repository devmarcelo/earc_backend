from django.db import models
from django.utils import timezone

class SchedulerControl(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_paused = models.BooleanField(default=False)
    class Meta:
        db_table = "ai_scheduler_control"
    @classmethod
    def paused(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj.is_paused

class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    handler = models.CharField(max_length=255)
    args = models.JSONField(default=dict, blank=True)
    tenant_schema = models.CharField(max_length=63, null=True, blank=True)
    interval_seconds = models.PositiveIntegerField(default=5)
    enabled = models.BooleanField(default=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    lock_until = models.DateTimeField(null=True, blank=True)
    max_runtime_seconds = models.PositiveIntegerField(default=55)
    consecutive_failures = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "ai_job"

    def schedule_next(self):
        now = timezone.now()
        self.next_run_at = now + timezone.timedelta(seconds=self.interval_seconds)
        self.save(update_fields=["next_run_at"])
