from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = router.urls
