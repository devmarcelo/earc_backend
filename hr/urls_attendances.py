from rest_framework.routers import DefaultRouter
from hr.views import AttendanceViewSet

router = DefaultRouter()
router.register(r'', AttendanceViewSet, basename='attendance')

urlpatterns = router.urls
