# reports/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MetaResultadoViewSet, ProjecaoCaixaViewSet, 
    FinancialSummaryView, CashFlowReportView, ExpenseByCategoryReportView
)

router = DefaultRouter()
router.register(r"metas-resultados", MetaResultadoViewSet, basename="metaresultado")
router.register(r"projecoes-caixa", ProjecaoCaixaViewSet, basename="projecaocaixa")

urlpatterns = [
    path("", include(router.urls)),
    # Report generation endpoints
    path("summary/<int:year>/<int:month>/", FinancialSummaryView.as_view(), name="financial-summary"),
    path("cash-flow/", CashFlowReportView.as_view(), name="cash-flow-report"),
    path("expenses-by-category/", ExpenseByCategoryReportView.as_view(), name="expense-by-category-report"),
]

