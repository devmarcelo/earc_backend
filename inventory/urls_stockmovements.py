from rest_framework.routers import DefaultRouter
from inventory.views import StockMovementViewSet

router = DefaultRouter()
router.register(r'', StockMovementViewSet, basename='stockmovement')

urlpatterns = router.urls
