from rest_framework.routers import DefaultRouter
from inventory.views import InventoryCountViewSet

router = DefaultRouter()
router.register(r'', InventoryCountViewSet, basename='inventorycount')

urlpatterns = router.urls
