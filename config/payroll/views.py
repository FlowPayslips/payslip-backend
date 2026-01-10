from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Payrun, Payslip
from .serializers import PayrunSerializer, PayslipSerializer
from core.permissions import IsCompanyMember
from accounts.permissions import IsAdminUser
from .permissions import IsPayslipOwner

class PayrunViewSet(ReadOnlyModelViewSet):
    serializer_class = PayrunSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember, IsAdminUser]

    def get_queryset(self):
        return Payrun.objects.filter(
            company=self.request.user.employee.company
        )

class PayslipViewSet(ReadOnlyModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        employee = user.employee

        if user.is_staff:
            return Payslip.objects.filter(
                payrun__company=employee.company
            )

        return Payslip.objects.filter(employee=employee)