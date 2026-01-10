from rest_framework import serializers
from .models import Payrun, Payslip


class PayrunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payrun
        fields = (
            "id",
            "month",
            "year",
            "status",
            "processed_at",
            "created_at",
        )


class PayslipSerializer(serializers.ModelSerializer):
    payrun = PayrunSerializer(read_only=True)

    class Meta:
        model = Payslip
        fields = (
            "id",
            "payrun",
            "basic_pay",
            "allowances",
            "deductions",
            "net_pay",
            "generated_at",
        )
