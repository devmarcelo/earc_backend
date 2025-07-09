from django.urls import path, include

urlpatterns = [
    path('parameters/', include('settings_app.urls_parameters')),
    path('integrations/', include('settings_app.urls_integrations')),
    # Adicione outros domínios aqui conforme crescer (ex: themes, preferences, etc)
]
