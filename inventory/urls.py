from django.urls import path, include

urlpatterns = [
    path('products/', include('inventory.urls_products')),
    path('stockmovements/', include('inventory.urls_stockmovements')),
    path('inventorycounts/', include('inventory.urls_inventorycounts')),
    # Adicione outros domínios aqui conforme o sistema crescer
]
