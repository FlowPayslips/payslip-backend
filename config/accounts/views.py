from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MeSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = request.user.employee
        serializer = MeSerializer(
            {
                "user": request.user,
                "employee": employee,
            }
        )
        return Response(serializer.data)
