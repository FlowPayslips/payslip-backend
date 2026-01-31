from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Company, Employee
from .serializers import CompanySerializer
from .permissions import IsCompanyMember
from .serializers import EmployeeSerializer, EmployeeInviteSerializer, AcceptInviteSerializer

from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdmin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

class CompanyViewSet(ReadOnlyModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Company.objects.filter(
            id=self.request.user.employee.company_id
        )


class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsCompanyMember, IsAdmin]

    def get_queryset(self):
        return Employee.objects.filter(
            company=self.request.user.employee.company
        )

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeeInviteSerializer
        return EmployeeSerializer

class AcceptInviteView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=AcceptInviteSerializer,
        responses={200: None},
        auth=None,
    )

    def post(self, request):
        serializer = AcceptInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Invite accepted successfully."},
            status=status.HTTP_200_OK,
        )