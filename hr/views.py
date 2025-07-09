from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Employee, Payroll, Attendance
from .serializers import EmployeeSerializer, PayrollSerializer, AttendanceSerializer
from core.views import TenantAwareViewSet

class EmployeeViewSet(TenantAwareViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = {
        "name": ["exact", "icontains"],
        "document": ["exact"],
        "job_title": ["exact", "icontains"],
        "hire_date": ["exact", "gte", "lte"],
        "termination_date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["name", "document", "job_title", "email", "phone"]

class PayrollViewSet(TenantAwareViewSet):
    queryset = Payroll.objects.select_related("employee")
    serializer_class = PayrollSerializer
    filterset_fields = {
        "employee": ["exact"],
        "period": ["exact"],
        "payment_date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["employee__name", "period", "notes"]

class AttendanceViewSet(TenantAwareViewSet):
    queryset = Attendance.objects.select_related("employee")
    serializer_class = AttendanceSerializer
    filterset_fields = {
        "employee": ["exact"],
        "date": ["exact", "gte", "lte"],
        "is_active": ["exact"],
    }
    search_fields = ["employee__name", "date", "notes"]
