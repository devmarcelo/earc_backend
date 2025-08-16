from django.contrib import admin
from .models import Job, SchedulerControl

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("name","enabled","tenant_schema","interval_seconds","next_run_at","last_run_at","consecutive_failures")
    list_editable = ("enabled","interval_seconds")
    search_fields = ("name","handler","tenant_schema")
    readonly_fields = ("next_run_at","last_run_at","lock_until","consecutive_failures")

@admin.register(SchedulerControl)
class SchedulerControlAdmin(admin.ModelAdmin):
    list_display = ("is_paused",)
    list_editable = ("is_paused",)
