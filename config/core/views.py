from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Company, Employee
from .serializers import CompanySerializer
from .permissions import IsCompanyMember
from .serializers import EmployeeSerializer, EmployeeInviteSerializer

from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdminUser

class CompanyViewSet(ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Company.objects.filter(
            id=self.request.user.employee.company_id
        )


class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsCompanyMember, IsAdminUser]

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.user.employee.company
        )

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeeInviteSerializer
        return EmployeeSerializer
