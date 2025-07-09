from rest_framework.routers import DefaultRouter
from financial.views import ExpenseViewSet

router = DefaultRouter()
router.register(r'', ExpenseViewSet, basename='expense')

urlpatterns = router.urls
