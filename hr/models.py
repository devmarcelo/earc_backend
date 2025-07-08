from django.db import models
from core.models import TenantAwareModel

class Employee(TenantAwareModel):
    name = models.CharField(max_length=150)
    document = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'document']),
            models.Index(fields=['tenant', 'name']),
        ]
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def anonymize(self):
        self.name = ""
        self.document = ""
        self.email = ""
        self.phone = ""
        self.job_title = ""
        self.notes = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name

class Payroll(TenantAwareModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period = models.CharField(max_length=7)  # e.g., "2024-07"
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'period']),
        ]
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'

    def __str__(self):
        return f"{self.employee} - {self.period}"

class Attendance(TenantAwareModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(blank=True, null=True)
    lunch_start = models.TimeField(blank=True, null=True)
    lunch_end = models.TimeField(blank=True, null=True)
    check_out = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'employee']),
            models.Index(fields=['tenant', 'date']),
        ]
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.employee} - {self.date}"
