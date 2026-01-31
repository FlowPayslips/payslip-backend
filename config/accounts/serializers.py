from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Employee, Company

User = get_user_model()


class MeSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    is_staff = serializers.BooleanField(source="user.is_staff")

    employee_id = serializers.CharField(source="employee.employee_id")
    company_id = serializers.IntegerField(source="employee.company.id")
    company_name = serializers.CharField(source="employee.company.name")
    role = serializers.CharField(source="employee.role")
    onboarding_status = serializers.CharField(source="employee.onboarding_status")