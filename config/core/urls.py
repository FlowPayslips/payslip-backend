from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, EmployeeViewSet

router = DefaultRouter()
router.register("companies", CompanyViewSet, basename="company")
router.register("employees", EmployeeViewSet, basename="employee")

urlpatterns = router.urls
