from rest_framework.routers import DefaultRouter
from financial.views import CustomerViewSet

router = DefaultRouter()
router.register(r'', CustomerViewSet, basename='customer')

urlpatterns = router.urls
