from rest_framework.routers import DefaultRouter
from .views import PayrunViewSet, PayslipViewSet

router = DefaultRouter()
router.register("payruns", PayrunViewSet, basename="payrun")
router.register("payslips", PayslipViewSet, basename="payslip")

urlpatterns = router.urls
