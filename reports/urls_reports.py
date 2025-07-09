from rest_framework.routers import DefaultRouter
from reports.views import ReportViewSet

router = DefaultRouter()
router.register(r'', ReportViewSet, basename='report')

urlpatterns = router.urls
