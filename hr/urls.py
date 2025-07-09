from django.urls import path, include

urlpatterns = [
    path('employees/', include('hr.urls_employees')),
    path('payrolls/', include('hr.urls_payrolls')),
    path('attendances/', include('hr.urls_attendances')),
    # Adicione outros domínios aqui conforme o sistema crescer (ex: leaves, benefits, etc)
]
