from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, EmployeeViewSet, AcceptInviteView
from django.urls import path

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("employees", EmployeeViewSet, basename="employee")

urlpatterns = router.urls


urlpatterns += [
    path("invites/accept/", AcceptInviteView.as_view(), name="accept-invite"),
]