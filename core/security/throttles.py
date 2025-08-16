# core/security/throttles.py
from rest_framework.throttling import SimpleRateThrottle

def _ident(request):
    ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    tenant = getattr(getattr(request, "tenant", None), "schema_name", "public")
    user_id = getattr(getattr(request, "user", None), "pk", "anon")
    return f"{tenant}:{user_id}:{ip}"

class LoginRateThrottle(SimpleRateThrottle):
    scope = "auth_login"
    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': _ident(request)}

class ResetRateThrottle(SimpleRateThrottle):
    scope = "auth_reset"
    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': _ident(request)}
