from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from .permissions import IsCompanyMember


class CompanyViewSet(ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Company.objects.filter(
            id=self.request.user.employee.company_id
        )


class EmployeeViewSet(ReadOnlyModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.user.employee.company
        )
