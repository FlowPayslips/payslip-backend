from django.db import models
from core.models import Company, Employee


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
        Employee, on_delete=models.CASCADE, related_name="payslips"
    )
    payrun = models.ForeignKey(
        Payrun, on_delete=models.CASCADE, related_name="payslips"
    )

    basic_pay = models.DecimalField(max_digits=12, decimal_places=2)
    allowances = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    deductions = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)

    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "payrun")

    def __str__(self):
        return f"{self.employee} - {self.payrun}"
