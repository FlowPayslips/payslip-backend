from rest_framework.permissions import BasePermission
from core.models import Employee


class IsCompanyMember(BasePermission):
    def has_permission(self, request, view):
        print(request.user, hasattr(request.user, "employee"))
        return hasattr(request.user, "employee")

    def has_object_permission(self, request, view, obj):
        return obj.company == request.user.employee.company



class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        employee = getattr(request.user, "employee", None)
        return (
            employee
            and employee.is_active
            and employee.role == Employee.ROLE_ADMIN
        )


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        employee = getattr(request.user, "employee", None)
        return (
            employee
            and employee.is_active
            and employee.role == Employee.ROLE_ACCOUNTANT
        )


class IsAdminOrAccountant(BasePermission):
    def has_permission(self, request, view):
        employee = getattr(request.user, "employee", None)
        return (
            employee
            and employee.is_active
            and employee.role
            in (Employee.ROLE_ADMIN, Employee.ROLE_ACCOUNTANT)
        )
