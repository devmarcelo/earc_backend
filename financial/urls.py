# financial/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, FornecedorViewSet, ReceitaViewSet, DespesaViewSet, ContaPagarReceberViewSet

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"fornecedores", FornecedorViewSet, basename="fornecedor")
router.register(r"receitas", ReceitaViewSet, basename="receita")
router.register(r"despesas", DespesaViewSet, basename="despesa")
router.register(r"contas", ContaPagarReceberViewSet, basename="conta")

urlpatterns = [
    path("", include(router.urls)),
]

