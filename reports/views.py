from rest_framework import views, permissions, status, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date

from .models import Report
from .serializers import (
    ReportSerializer,
    FinancialSummarySerializer,
    CashFlowReportSerializer,
    ExpenseByCategoryReportSerializer
)
from core.views import TenantAwareViewSet

# --- CRUD para reports persistidos ---
class ReportViewSet(TenantAwareViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filterset_fields = {
        "report_type": ["exact", "icontains"],
        "is_active": ["exact"],
        "generated_at": ["exact", "gte", "lte", "date__year", "date__month"],
    }
    search_fields = ["name", "description", "report_type"]

# --- API Views para relatórios dinâmicos/analytics ---

class FinancialSummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, year, month, format=None):
        # TODO: Implement logic using a ReportService
        summary_data = {
            "month": month,
            "year": year,
            "total_revenue": 10000.50,
            "total_expense": 7500.25,
            "net_profit_loss": 2500.25,
            "profit_margin_percent": 25.00,
            "target_profit": 2000.00,
            "target_achieved_percent": 125.01,
            "open_accounts_value": 1500.00,
            "total_inventory_value": 5000.00
        }
        serializer = FinancialSummarySerializer(summary_data)
        return Response(serializer.data)

class CashFlowReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        report_data = {
            "start_date": start_date,
            "end_date": end_date,
            "initial_balance": 1000.00,
            "entries": [
                {"date": "2024-01-01", "inflow": 500.00, "outflow": 100.00, "daily_balance": 1400.00},
                {"date": "2024-01-02", "inflow": 0.00, "outflow": 50.00, "daily_balance": 1350.00},
            ],
            "final_balance": 1350.00
        }

        serializer = CashFlowReportSerializer(report_data)
        return Response(serializer.data)

class ExpenseByCategoryReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        report_data = {
            "start_date": start_date,
            "end_date": end_date,
            "entries": [
                {"category_id": 1, "category_name": "Rent", "total_value": 1200.00},
                {"category_id": 2, "category_name": "Office Supplies", "total_value": 150.75},
            ]
        }

        serializer = ExpenseByCategoryReportSerializer(report_data)
        return Response(serializer.data)
