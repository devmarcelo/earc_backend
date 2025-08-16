from django.http import JsonResponse
from django.urls import path

def health(_request):
    return JsonResponse({"status": "ok", "service": "operator"}, status=200)

urlpatterns = [
    path("health/", health, name="op-health"),
]
