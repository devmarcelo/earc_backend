from django.contrib import admin
from .models import Employee, Payroll, Attendance

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "document", "job_title", "email", "phone", "tenant", "is_active", "created_on")
    search_fields = ("name", "document", "email", "phone", "job_title")
    list_filter = ("tenant", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on", "is_anonymized")

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ("employee", "period", "base_salary", "net_salary", "payment_date", "tenant", "is_active", "created_on")
    search_fields = ("employee__name", "period")
    list_filter = ("tenant", "period", "is_active", "payment_date")
    readonly_fields = ("tenant", "created_on", "updated_on")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "check_in", "lunch_start", "lunch_end", "check_out", "tenant", "is_active", "created_on")
    search_fields = ("employee__name", "date")
    list_filter = ("tenant", "date", "is_active")
    readonly_fields = ("tenant", "created_on", "updated_on")
