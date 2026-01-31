from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Payrun, Payslip
from .serializers import PayrunSerializer, PayslipSerializer, PayrunCreateSerializer
from core.permissions import IsCompanyMember
from core.permissions import IsAdmin
from .permissions import IsPayslipOwner
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from drf_spectacular.utils import extend_schema
from core.models import Employee

class PayrunViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsCompanyMember, IsAdmin]

    def get_queryset(self):
        return Payrun.objects.filter(
            company=self.request.user.employee.company
        )

    def get_serializer_class(self):
        if self.action == "create":
            return PayrunCreateSerializer
        return PayrunSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payrun = serializer.save()
        return Response(
            PayrunSerializer(payrun).data,
            status=status.HTTP_201_CREATED,
        )
    
    @extend_schema(
        request=None,
        responses={200: None},
    )
    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        payrun = self.get_object()

        if payrun.status != Payrun.STATUS_DRAFT:
            return Response(
                {"detail": "Payrun is not in draft state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            employees = Employee.objects.filter(
                company=payrun.company, is_active=True
            )

            for employee in employees:
                Payslip.objects.create(
                    employee=employee,
                    payrun=payrun,
                    basic_pay=0,
                    allowances=0,
                    deductions=0,
                    net_pay=0,
                )

            payrun.status = Payrun.STATUS_PROCESSED
            payrun.processed_at = timezone.now()
            payrun.save(update_fields=["status", "processed_at"])

        return Response({"detail": "Payrun processed."})
    
    @extend_schema(
        request=None,
        responses={200: None},
    )
    @action(detail=True, methods=["post"])
    def lock(self, request, pk=None):
        payrun = self.get_object()

        if payrun.status != Payrun.STATUS_PROCESSED:
            return Response(
                {"detail": "Only processed payruns can be locked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payrun.status = Payrun.STATUS_LOCKED
        payrun.save(update_fields=["status"])

        return Response({"detail": "Payrun locked."})


class PayslipViewSet(ReadOnlyModelViewSet):
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        user = self.request.user
        employee = user.employee

        if user.is_staff:
            return Payslip.objects.filter(
                payrun__company=employee.company
            )

        return Payslip.objects.filter(employee=employee)