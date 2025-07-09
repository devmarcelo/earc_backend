from rest_framework.routers import DefaultRouter
from financial.views import TransferViewSet

router = DefaultRouter()
router.register(r'', TransferViewSet, basename='transfer')

urlpatterns = router.urls
