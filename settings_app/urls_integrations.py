from rest_framework.routers import DefaultRouter
from settings_app.views import IntegrationViewSet

router = DefaultRouter()
router.register(r'', IntegrationViewSet, basename='integration')

urlpatterns = router.urls
