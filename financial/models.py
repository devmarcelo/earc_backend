from django.db import models
from core.models import TenantAwareModel

class Customer(TenantAwareModel):
    name = models.CharField(max_length=150)
    document = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        unique_together = (('tenant', 'document'),)
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'document']),
        ]
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def anonymize(self):
        self.name = ""
        self.document = ""
        self.email = ""
        self.phone = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name

class Supplier(TenantAwareModel):
    name = models.CharField(max_length=150)
    document = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        unique_together = (('tenant', 'document'),)
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'document']),
        ]
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def anonymize(self):
        self.name = ""
        self.document = ""
        self.email = ""
        self.phone = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return self.name

class Category(TenantAwareModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['tenant', 'is_active'])]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class BankAccount(TenantAwareModel):
    name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    branch = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20)
    initial_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'name']),
        ]
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

    def __str__(self):
        return f"{self.name} - {self.bank}"

class Expense(TenantAwareModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    paid = models.BooleanField(default=False)
    account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    document = models.CharField(max_length=100)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        unique_together = (('tenant', 'document'),)
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'document']),
        ]
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def anonymize(self):
        self.document = ""
        self.description = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return f"{self.category} - {self.amount}"

class Revenue(TenantAwareModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    received = models.BooleanField(default=False)
    account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    document = models.CharField(max_length=100)
    is_anonymized = models.BooleanField(default=False)

    class Meta:
        unique_together = (('tenant', 'document'),)
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'document']),
        ]
        verbose_name = 'Revenue'
        verbose_name_plural = 'Revenues'

    def anonymize(self):
        self.document = ""
        self.description = ""
        self.is_anonymized = True
        self.save()

    def __str__(self):
        return f"{self.category} - {self.amount}"

class Transfer(TenantAwareModel):
    source_account = models.ForeignKey(BankAccount, related_name='outgoing_transfers', on_delete=models.PROTECT)
    destination_account = models.ForeignKey(BankAccount, related_name='incoming_transfers', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'source_account', 'destination_account']),
        ]
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return f"{self.source_account} -> {self.destination_account} - {self.amount}"
