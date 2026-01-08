from rest_framework import serializers
from .models import Company, Employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "name", "is_active", "created_at")


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "company",
            "employee_id",
            "is_active",
            "joined_at",
        )
