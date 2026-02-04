from django.contrib import admin
from .models import Payrun, Payslip, PayslipLineItem, SalaryComponent, EmployeeSalaryComponent


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
        "net_pay",
        "generated_at",
    )
    list_filter = ("payrun__company", "payrun__year")

@admin.register(PayslipLineItem)
class PayslipLineItemAdmin(admin.ModelAdmin):
    list_display = (
        "payslip",
        "component_code",
        "component_type",
        "amount",
    )
    list_filter = ("component_type",)
    search_fields = ("component_code", "component_name")

@admin.register(SalaryComponent)
class SalaryComponentAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "name",
        "code",
        "component_type",
        "is_taxable",
        "is_active",
    )
    list_filter = ("company", "component_type")


@admin.register(EmployeeSalaryComponent)
class EmployeeSalaryComponentAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "component",
        "amount",
        "is_active",
    )
    list_filter = ("component__company", "component__component_type", "is_active")
    search_fields = ("employee__employee_id", "component__code")