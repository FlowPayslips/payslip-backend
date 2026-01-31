from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_EMPLOYEE = "employee"
    ROLE_ADMIN = "admin"
    ROLE_ACCOUNTANT = "accountant"

    ROLE_CHOICES = (
        (ROLE_EMPLOYEE, "Employee"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_ACCOUNTANT, "Accountant"),
    )

    ONBOARDING_INVITED = "invited"
    ONBOARDING_ONBOARDED = "onboarded"

    ONBOARDING_STATUS_CHOICES = (
        (ONBOARDING_INVITED, "Invited"),
        (ONBOARDING_ONBOARDED, "Onboarded"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )
    employee_id = models.CharField(max_length=50)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_EMPLOYEE,
    )

    onboarding_status = models.CharField(
        max_length=20,
        choices=ONBOARDING_STATUS_CHOICES,
        default=ONBOARDING_INVITED,
    )

    is_active = models.BooleanField(default=True)
    joined_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"

class Invite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="invites"
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_invites",
    )

    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("email", "company")

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_accepted(self):
        return self.accepted_at is not None

    def __str__(self):
        return f"{self.email} -> {self.company.name}"
