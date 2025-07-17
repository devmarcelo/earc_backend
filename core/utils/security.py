# core/utils/security.py

from django.core.cache import cache

MAX_REFRESH_ATTEMPTS = 5
BLOCK_TIME_SECONDS = 60 * 10  # 10 minutos

def _make_token_key(token, tenant):
    return f"refresh_attempts:{tenant.schema_name if tenant else 'public'}:{token}"

def register_token_attempt(token, tenant, success):
    """
    Incrementa tentativas, bloqueia após muitas falhas.
    """
    key = _make_token_key(token, tenant)
    if success:
        cache.delete(key)
    else:
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, BLOCK_TIME_SECONDS)
        if attempts >= MAX_REFRESH_ATTEMPTS:
            cache.set(f"{key}:blocked", True, BLOCK_TIME_SECONDS)

def is_token_blocked(token, tenant):
    key = _make_token_key(token, tenant)
    return cache.get(f"{key}:blocked", False)
