from rest_framework import serializers
from .models import Payrun, Payslip
from rest_framework import serializers
from .models import Payslip, PayslipLineItem


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

class PayrunCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payrun
        fields = ("month", "year")

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["company"] = request.user.employee.company
        return super().create(validated_data)


class PayslipLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayslipLineItem
        fields = (
            "component_name",
            "component_code",
            "component_type",
            "amount",
        )

class PayslipDetailSerializer(serializers.ModelSerializer):
    payrun_month = serializers.IntegerField(source="payrun.month")
    payrun_year = serializers.IntegerField(source="payrun.year")
    company_name = serializers.CharField(
        source="payrun.company.name"
    )
    employee_id = serializers.CharField(
        source="employee.employee_id"
    )
    line_items = PayslipLineItemSerializer(many=True)

    class Meta:
        model = Payslip
        fields = (
            "id",
            "company_name",
            "employee_id",
            "payrun_month",
            "payrun_year",
            "basic_pay",
            "deductions",
            "net_pay",
            "generated_at",
            "line_items",
        )
