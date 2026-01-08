from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )
    employee_id = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company.name}"
