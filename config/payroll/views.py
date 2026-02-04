from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import PayrunSerializer, PayslipSerializer, PayrunCreateSerializer, PayslipDetailSerializer
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

from decimal import Decimal
from payroll.models import (
    Payrun,
    Payslip,
    PayslipLineItem,
    EmployeeSalaryComponent,
)

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
    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        payrun = self.get_object()

        # 1. State guard
        if payrun.status != Payrun.STATUS_DRAFT:
            return Response(
                {"detail": "Payrun is not in draft state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Prevent double processing
        if payrun.payslips.exists():
            return Response(
                {"detail": "Payslips already generated for this payrun."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employees = Employee.objects.filter(
            company=payrun.company,
            is_active=True,
            onboarding_status=Employee.ONBOARDING_ONBOARDED,
        )

        if not employees.exists():
            return Response(
                {"detail": "No onboarded employees found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            for employee in employees:
                print(employee)
                assignments = (
                    EmployeeSalaryComponent.objects.filter(
                        employee=employee,
                        is_active=True,
                        component__is_active=True,
                    )
                    .select_related("component")
                )

                if not assignments.exists():
                    raise ValueError(
                        f"No salary components configured for employee {employee.id}"
                    )

                total_earnings = Decimal("0.00")
                total_deductions = Decimal("0.00")

                payslip = Payslip.objects.create(
                    employee=employee,
                    payrun=payrun,
                    total_earnings=Decimal("0.00"),
                    total_deductions=Decimal("0.00"),
                    net_pay=Decimal("0.00"),
                )

                for assignment in assignments:
                    component = assignment.component
                    amount = assignment.amount

                    PayslipLineItem.objects.create(
                        payslip=payslip,
                        component_name=component.name,
                        component_code=component.code,
                        component_type=component.component_type,
                        component_id=component.id,
                        amount=amount,
                    )

                    if component.component_type == component.TYPE_EARNING:
                        total_earnings += amount
                    else:
                        total_deductions += amount

                payslip.total_earnings = total_earnings
                payslip.total_deductions = total_deductions
                payslip.net_pay = total_earnings - total_deductions
                payslip.save(
                    update_fields=[
                        "total_earnings",
                        "total_deductions",
                        "net_pay",
                    ]
                )

            payrun.status = Payrun.STATUS_PROCESSED
            payrun.processed_at = timezone.now()
            payrun.save(update_fields=["status", "processed_at"])

        return Response(
            {"detail": "Payrun processed successfully."},
            status=status.HTTP_200_OK,
        )

    
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        employee = user.employee

        qs = Payslip.objects.select_related(
            "employee",
            "payrun",
            "payrun__company",
        ).prefetch_related("line_items")

        if employee.role in ["admin", "accountant"]:
            return qs.filter(
                payrun__company=employee.company
            )

        return qs.filter(employee=employee)

    def get_serializer_class(self):
        print(self.action)
        if self.action == "retrieve":
            return PayslipDetailSerializer
        return PayslipSerializer
