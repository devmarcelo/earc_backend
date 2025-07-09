from django.urls import path
from reports.views import (
    FinancialSummaryView,
    CashFlowReportView,
    ExpenseByCategoryReportView,
)

urlpatterns = [
    path("summary/<int:year>/<int:month>/", FinancialSummaryView.as_view(), name="financial-summary"),
    path("cash-flow/", CashFlowReportView.as_view(), name="cash-flow-report"),
    path("expenses-by-category/", ExpenseByCategoryReportView.as_view(), name="expense-by-category-report"),
]
