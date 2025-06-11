# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemEstoqueViewSet

router = DefaultRouter()
router.register(r"itens", ItemEstoqueViewSet, basename="itemestoque")

urlpatterns = [
    path("", include(router.urls)),
]

