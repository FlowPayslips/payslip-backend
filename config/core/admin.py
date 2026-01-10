from django.contrib import admin
from .models import Company, Employee, Invite


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "employee_id", "is_active")
    search_fields = ("employee_id", "user__username")

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "company",
        "invited_by",
        "created_at",
        "expires_at",
        "accepted_at",
    )
    search_fields = ("email",)
    list_filter = ("company", "accepted_at")