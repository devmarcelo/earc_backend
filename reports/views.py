# reports/views.py
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from django.http import Http404

from .models import MetaResultado, ProjecaoCaixa
from .serializers import (
    MetaResultadoSerializer, ProjecaoCaixaSerializer,
    FinancialSummarySerializer, CashFlowReportSerializer, ExpenseByCategoryReportSerializer
)
from core.views import TenantAwareViewSet # Reuse base viewset
# Import services later when created
# from .services import ReportService 

class MetaResultadoViewSet(TenantAwareViewSet):
    queryset = MetaResultado.objects.all()
    serializer_class = MetaResultadoSerializer
    filterset_fields = {
        "mes_ano": ["exact", "gte", "lte", "year", "month"],
    }
    # Add search fields if needed

class ProjecaoCaixaViewSet(TenantAwareViewSet):
    queryset = ProjecaoCaixa.objects.all()
    serializer_class = ProjecaoCaixaSerializer
    filterset_fields = {
        "data": ["exact", "gte", "lte", "year", "month"],
    }
    # Add search fields if needed

# --- API Views for Generated Reports ---

class FinancialSummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Add IsTenantMember later

    def get(self, request, year, month, format=None):
        # TODO: Implement logic using a ReportService
        # report_service = ReportService(request.tenant)
        # summary_data = report_service.get_financial_summary(year, month)
        
        # Placeholder data
        summary_data = {
            "month": month,
            "year": year,
            "receita_total": 10000.50,
            "despesa_total": 7500.25,
            "lucro_prejuizo": 2500.25,
            "margem_lucro_percentual": 25.00,
            "meta_lucro": 2000.00,
            "meta_atingida_percentual": 125.01,
            "contas_em_aberto_valor": 1500.00,
            "total_estoque_valor": 5000.00
        }
        
        serializer = FinancialSummarySerializer(summary_data)
        return Response(serializer.data)

class CashFlowReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Add IsTenantMember later

    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Implement logic using a ReportService
        # report_service = ReportService(request.tenant)
        # report_data = report_service.get_cash_flow_report(start_date, end_date)

        # Placeholder data
        report_data = {
            "start_date": start_date,
            "end_date": end_date,
            "saldo_inicial": 1000.00,
            "entries": [
                {"data": "2024-01-01", "entrada": 500.00, "saida": 100.00, "saldo_diario": 1400.00},
                {"data": "2024-01-02", "entrada": 0.00, "saida": 50.00, "saldo_diario": 1350.00},
            ],
            "saldo_final": 1350.00
        }

        serializer = CashFlowReportSerializer(report_data)
        return Response(serializer.data)

class ExpenseByCategoryReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Add IsTenantMember later

    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        if not start_date_str or not end_date_str:
            return Response({"error": "start_date and end_date query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Implement logic using a ReportService
        # report_service = ReportService(request.tenant)
        # report_data = report_service.get_expense_by_category_report(start_date, end_date)

        # Placeholder data
        report_data = {
            "start_date": start_date,
            "end_date": end_date,
            "entries": [
                {"categoria_id": 1, "categoria_nome": "Aluguel", "total_valor": 1200.00},
                {"categoria_id": 2, "categoria_nome": "Material Escritório", "total_valor": 150.75},
            ]
        }

        serializer = ExpenseByCategoryReportSerializer(report_data)
        return Response(serializer.data)

