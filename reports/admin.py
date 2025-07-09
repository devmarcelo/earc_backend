from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("name", "report_type", "generated_at", "tenant", "is_active", "created_on")
    search_fields = ("name", "report_type", "description")
    list_filter = ("tenant", "report_type", "is_active", "generated_at")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")
