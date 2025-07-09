from rest_framework.routers import DefaultRouter
from financial.views import SupplierViewSet

router = DefaultRouter()
router.register(r'', SupplierViewSet, basename='supplier')

urlpatterns = router.urls
