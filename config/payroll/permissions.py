from rest_framework.permissions import BasePermission


class IsPayslipOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.employee.user == request.user
