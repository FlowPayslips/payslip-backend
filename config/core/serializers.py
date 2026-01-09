from rest_framework import serializers
from .models import Company, Employee

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Employee

User = get_user_model()

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

class EmployeeInviteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Employee
        fields = ("email", "employee_id", "joined_at")

    def validate_email(self, email):
        request = self.context["request"]
        company = request.user.employee.company

        if Employee.objects.filter(
            user__email=email, company=company
        ).exists():
            raise serializers.ValidationError(
                "User is already an employee of this company."
            )

        return email

    def create(self, validated_data):
        request = self.context["request"]
        company = request.user.employee.company
        email = validated_data.pop("email")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "is_active": False,
            },
        )

        employee = Employee.objects.create(
            user=user,
            company=company,
            **validated_data,
        )

        # invite token + email sending will hook in here later

        return employee
