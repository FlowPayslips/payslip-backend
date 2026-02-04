from django.db import models
from core.models import Company, Employee
from decimal import Decimal

class Payrun(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PROCESSED = "processed"
    STATUS_LOCKED = "locked"

    STATUS_CHOICES = (
        (STATUS_DRAFT, "Draft"),
        (STATUS_PROCESSED, "Processed"),
        (STATUS_LOCKED, "Locked"),
    )

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="payruns"
    )
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "month", "year")
        ordering = ("-year", "-month")

    def __str__(self):
        return f"{self.company.name} - {self.month}/{self.year}"

class Payslip(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payslips",
    )
    payrun = models.ForeignKey(
        Payrun,
        on_delete=models.CASCADE,
        related_name="payslips",
    )

    total_earnings = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    total_deductions = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    net_pay = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "payrun")

    def __str__(self):
        return f"{self.employee} - {self.payrun}"


class PayslipLineItem(models.Model):
    TYPE_EARNING = "earning"
    TYPE_DEDUCTION = "deduction"

    TYPE_CHOICES = (
        (TYPE_EARNING, "Earning"),
        (TYPE_DEDUCTION, "Deduction"),
    )

    payslip = models.ForeignKey(
        Payslip,
        on_delete=models.CASCADE,
        related_name="line_items",
    )

    # snapshot fields (authoritative)
    component_name = models.CharField(max_length=100)
    component_code = models.CharField(max_length=50)
    component_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    # optional traceability (never used for logic)
    component_id = models.IntegerField(null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.component_code} - {self.amount}"


class SalaryComponent(models.Model):
    TYPE_EARNING = "earning"
    TYPE_DEDUCTION = "deduction"

    TYPE_CHOICES = (
        (TYPE_EARNING, "Earning"),
        (TYPE_DEDUCTION, "Deduction"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_components",
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    component_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    is_taxable = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "code")
        ordering = ("component_type", "name")

    def __str__(self):
        return f"{self.company.name} - {self.code}"


class EmployeeSalaryComponent(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_components",
    )
    component = models.ForeignKey(
        SalaryComponent,
        on_delete=models.CASCADE,
        related_name="employee_assignments",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("employee", "component")

    def __str__(self):
        return f"{self.employee} - {self.component.code}"