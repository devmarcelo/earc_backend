from rest_framework.routers import DefaultRouter
from settings_app.views import ParameterViewSet

router = DefaultRouter()
router.register(r'', ParameterViewSet, basename='parameter')

urlpatterns = router.urls
