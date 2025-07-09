from django.urls import path, include

urlpatterns = [
    path('reports/', include('reports.urls_reports')),
    path('analytics/', include('reports.urls_analytics')),
    # Adicione outros domínios aqui no futuro (ex: dashboard, export, etc)
]
