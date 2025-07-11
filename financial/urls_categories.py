# financial/urls_categories.py
from rest_framework.routers import DefaultRouter
from financial.views import CategoryViewSet

router = DefaultRouter()
router.register(r'', CategoryViewSet, basename='category')

urlpatterns = router.urls
