from rest_framework.routers import DefaultRouter
from financial.views import BankAccountViewSet

router = DefaultRouter()
router.register(r'', BankAccountViewSet, basename='bankaccount')

urlpatterns = router.urls
