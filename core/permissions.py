from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowOnlyGet(BasePermission):
    """
    Permite apenas métodos GET.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and request.method == "GET"