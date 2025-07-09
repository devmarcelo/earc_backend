from rest_framework.routers import DefaultRouter
from financial.views import RevenueViewSet

router = DefaultRouter()
router.register(r'', RevenueViewSet, basename='revenue')

urlpatterns = router.urls
