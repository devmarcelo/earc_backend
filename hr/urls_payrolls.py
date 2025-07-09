from rest_framework.routers import DefaultRouter
from hr.views import PayrollViewSet

router = DefaultRouter()
router.register(r'', PayrollViewSet, basename='payroll')

urlpatterns = router.urls
