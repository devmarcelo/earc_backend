from django.urls import path, include

urlpatterns = [
    path('categories/', include('financial.urls_categories')),
    path('customers/', include('financial.urls_customers')),
    path('suppliers/', include('financial.urls_suppliers')),
    path('bankaccounts/', include('financial.urls_bankaccounts')),
    path('expenses/', include('financial.urls_expenses')),
    path('revenues/', include('financial.urls_revenues')),
    path('transfers/', include('financial.urls_transfers')),
    # Add more domains here as needed
]
