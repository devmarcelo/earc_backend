from rest_framework import serializers
from .models import Employee, Payroll, Attendance

class EmployeeSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "name", "document", "job_title", "email", "phone",
            "hire_date", "termination_date", "notes", "is_active", "is_anonymized",
            "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "created_by", "updated_by", "tenant_id"
        ]

class PayrollSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = Payroll
        fields = [
            "id", "employee", "period", "base_salary", "deductions", "bonuses", "net_salary",
            "payment_date", "notes", "is_active",
            "created_on", "updated_on", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "tenant_id", "employee"
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)
    tenant_id = serializers.IntegerField(source='tenant.id', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "employee", "date", "check_in", "lunch_start", "lunch_end", "check_out", "notes", "is_active",
            "created_on", "updated_on", "tenant_id"
        ]
        read_only_fields = [
            "id", "created_on", "updated_on", "tenant_id", "employee"
        ]
