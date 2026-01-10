from django.contrib import admin
from .models import Payrun, Payslip


@admin.register(Payrun)
class PayrunAdmin(admin.ModelAdmin):
    list_display = ("company", "month", "year", "status", "processed_at")
    list_filter = ("company", "year", "status")
    ordering = ("-year", "-month")


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "payrun",
        "basic_pay",
        "net_pay",
        "generated_at",
    )
    list_filter = ("payrun__company", "payrun__year")
