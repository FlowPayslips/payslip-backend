from rest_framework import serializers
from .models import Company, Employee

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Employee, Invite
from datetime import timedelta
from django.utils import timezone
from .utils import generate_invite_token

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
            "onboarding_status",
            "role",
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

        if Invite.objects.filter(
            email=email, company=company, accepted_at__isnull=True
        ).exists():
            raise serializers.ValidationError(
                "An active invite already exists for this email."
            )

        return email

    def create(self, validated_data):
        request = self.context["request"]
        company = request.user.employee.company
        email = validated_data.pop("email")

        user, _ = User.objects.get_or_create(
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

        Invite.objects.create(
            email=email,
            company=company,
            invited_by=request.user,
            token=generate_invite_token(),
            expires_at=timezone.now() + timedelta(days=7),
        )

        return employee

class AcceptInviteSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        try:
            invite = Invite.objects.select_related("company").get(
                token=attrs["token"]
            )
        except Invite.DoesNotExist:
            raise serializers.ValidationError("Invalid invite token.")

        if invite.is_accepted():
            raise serializers.ValidationError("Invite already accepted.")

        if invite.is_expired():
            raise serializers.ValidationError("Invite has expired.")

        attrs["invite"] = invite
        return attrs

    def save(self):
        invite = self.validated_data["invite"]
        password = self.validated_data["password"]

        user = User.objects.get(email=invite.email)
        user.set_password(password)
        user.is_active = True
        user.save(update_fields=["password", "is_active"])

        invite.accepted_at = timezone.now()
        invite.save(update_fields=["accepted_at"])

        employee = Employee.objects.get(
            user=user,
            company=invite.company,
        )

        employee.onboarding_status = Employee.ONBOARDING_ONBOARDED
        employee.joined_at = timezone.now().date()
        employee.save(update_fields=["onboarding_status", "joined_at"])


        return user
