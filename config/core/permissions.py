from rest_framework.permissions import BasePermission


class IsCompanyMember(BasePermission):
    def has_permission(self, request, view):
        print(request.user, hasattr(request.user, "employee"))
        return hasattr(request.user, "employee")

    def has_object_permission(self, request, view, obj):
        return obj.company == request.user.employee.company
